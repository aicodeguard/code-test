    extra_skip_keys = get_settings().config.get('config.skip_keys', [])
    if extra_skip_keys:
        skip_keys.extend(extra_skip_keys)

    markdown_text = ""
    markdown_text += "\n<hr>\n<details> <summary><strong>🛠️ Relevant configurations:</strong></summary> \n\n"
    markdown_text +="<br>These are the relevant [configurations](https://github.com/Codium-ai/pr-agent/blob/main/pr_agent/settings/configuration.toml) for this tool:\n\n"
    markdown_text += f"**[config**]\n```yaml\n\n"
    for key, value in get_settings().config.items():
        if key in skip_keys:
            continue
        markdown_text += f"{key}: {value}\n"
    markdown_text += "\n```\n"
    markdown_text += f"\n**[{relevant_section}]**\n```yaml\n\n"
    for key, value in get_settings().get(relevant_section, {}).items():
        if key in skip_keys:
            continue
        markdown_text += f"{key}: {value}\n"
    markdown_text += "\n```"
    markdown_text += "\n</details>\n"
    return markdown_text

def is_value_no(value):
    if not value:
        return True
    value_str = str(value).strip().lower()
    if value_str == 'no' or value_str == 'none' or value_str == 'false':
        return True
    return False


def set_pr_string(repo_name, pr_number):
    return f"{repo_name}#{pr_number}"


def string_to_uniform_number(s: str) -> float:
    """
    Convert a string to a uniform number in the range [0, 1].
    The uniform distribution is achieved by the nature of the SHA-256 hash function, which produces a uniformly distributed hash value over its output space.
    """
    # Generate a hash of the string
    hash_object = hashlib.sha256(s.encode())
    # Convert the hash to an integer
    hash_int = int(hash_object.hexdigest(), 16)
    # Normalize the integer to the range [0, 1]
    max_hash_int = 2 ** 256 - 1
    uniform_number = float(hash_int) / max_hash_int
    return uniform_number


def process_description(description_full: str) -> Tuple[str, List]:
    if not description_full:
        return "", []

    description_split = description_full.split(PRDescriptionHeader.CHANGES_WALKTHROUGH.value)
    base_description_str = description_split[0]
    changes_walkthrough_str = ""
    files = []
    if len(description_split) > 1:
        changes_walkthrough_str = description_split[1]
    else:
        get_logger().debug("No changes walkthrough found")

    try:
        if changes_walkthrough_str:
            # get the end of the table
            if '</table>\n\n___' in changes_walkthrough_str:
                end = changes_walkthrough_str.index("</table>\n\n___")
            elif '\n___' in changes_walkthrough_str:
                end = changes_walkthrough_str.index("\n___")
            else:
                end = len(changes_walkthrough_str)
            changes_walkthrough_str = changes_walkthrough_str[:end]

            h = html2text.HTML2Text()
            h.body_width = 0  # Disable line wrapping

            # find all the files
            pattern = r'<tr>\s*<td>\s*(<details>\s*<summary>(.*?)</summary>(.*?)</details>)\s*</td>'
            files_found = re.findall(pattern, changes_walkthrough_str, re.DOTALL)
            for file_data in files_found:
                try:
                    if isinstance(file_data, tuple):
                        file_data = file_data[0]
                    pattern = r'<details>\s*<summary><strong>(.*?)</strong>\s*<dd><code>(.*?)</code>.*?</summary>\s*<hr>\s*(.*?)\s*<li>(.*?)</details>'
                    res = re.search(pattern, file_data, re.DOTALL)
                    if not res or res.lastindex != 4:
                        pattern_back = r'<details>\s*<summary><strong>(.*?)</strong><dd><code>(.*?)</code>.*?</summary>\s*<hr>\s*(.*?)\n\n\s*(.*?)</details>'
                        res = re.search(pattern_back, file_data, re.DOTALL)
                    if not res or res.lastindex != 4:
                        pattern_back = r'<details>\s*<summary><strong>(.*?)</strong>\s*<dd><code>(.*?)</code>.*?</summary>\s*<hr>\s*(.*?)\s*-\s*(.*?)\s*</details>' # looking for hypen ('- ')
                        res = re.search(pattern_back, file_data, re.DOTALL)
                    if res and res.lastindex == 4:
                        short_filename = res.group(1).strip()
                        short_summary = res.group(2).strip()
                        long_filename = res.group(3).strip()
                        long_summary =  res.group(4).strip()
                        long_summary = long_summary.replace('<br> *', '\n*').replace('<br>','').replace('\n','<br>')
                        long_summary = h.handle(long_summary).strip()
                        if long_summary.startswith('\\-'):
                            long_summary = "* " + long_summary[2:]
                        elif not long_summary.startswith('*'):
                            long_summary = f"* {long_summary}"

                        files.append({
                            'short_file_name': short_filename,
                            'full_file_name': long_filename,
                            'short_summary': short_summary,
                            'long_summary': long_summary
                        })
                    else:
                        if '<code>...</code>' in file_data:
                            pass # PR with many files. some did not get analyzed
                        else:
                            get_logger().error(f"Failed to parse description", artifact={'description': file_data})
                except Exception as e:
                    get_logger().exception(f"Failed to process description: {e}", artifact={'description': file_data})


    except Exception as e:
        get_logger().exception(f"Failed to process description: {e}")

    return base_description_str, files

def get_version() -> str:
    # First check pyproject.toml if running directly out of repository
    if os.path.exists("pyproject.toml"):
        if sys.version_info >= (3, 11):
            import tomllib
            with open("pyproject.toml", "rb") as f:
                data = tomllib.load(f)
                if "project" in data and "version" in data["project"]:
                    return data["project"]["version"]
                else:
                    get_logger().warning("Version not found in pyproject.toml")
        else:
            get_logger().warning("Unable to determine local version from pyproject.toml")

    # Otherwise get the installed pip package version
    try:
        return version('pr-agent')
    except PackageNotFoundError:
        get_logger().warning("Unable to find package named 'pr-agent'")
        return "unknown"


def set_file_languages(diff_files) -> List[FilePatchInfo]:
    try:
        # if the language is already set, do not change it
        if hasattr(diff_files[0], 'language') and diff_files[0].language:
            return diff_files

        # map file extensions to programming languages
        language_extension_map_org = get_settings().language_extension_map_org
        extension_to_language = {}
        for language, extensions in language_extension_map_org.items():
            for ext in extensions:
                extension_to_language[ext] = language
        for file in diff_files:
            extension_s = '.' + file.filename.rsplit('.')[-1]
            language_name = "txt"
            if extension_s and (extension_s in extension_to_language):
                language_name = extension_to_language[extension_s]
            file.language = language_name.lower()
    except Exception as e:
        get_logger().exception(f"Failed to set file languages: {e}")

    return diff_files
