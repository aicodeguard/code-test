# Language Selection, source: https://github.com/bigcode-project/bigcode-dataset/blob/main/language_selection/programming-languages-to-file-extensions.json  # noqa E501
from typing import Dict, List, TypeVar, Optional
from dataclasses import dataclass
from collections import defaultdict

from ai_review.config_loader import get_settings

FileType = TypeVar('FileType')  # 为文件对象创建类型变量

@dataclass
class LanguageGroup:
    language: str
    files: List[FileType]

def filter_bad_extensions(files: List[FileType]) -> List[FileType]:
    """过滤掉不需要的文件扩展名
    
    Args:
        files: 需要过滤的文件列表
    Returns:
        过滤后的文件列表
    """
    settings = get_settings()
    bad_extensions = settings.bad_extensions.default
    if settings.config.use_extra_bad_extensions:
        bad_extensions = bad_extensions + settings.bad_extensions.extra
    
    return [f for f in files if f.filename and is_valid_file(f.filename, bad_extensions)]


def is_valid_file(filename:str, bad_extensions=None) -> bool:
    if not filename:
        return False
    if not bad_extensions:
        bad_extensions = get_settings().bad_extensions.default
        if get_settings().config.use_extra_bad_extensions:
            bad_extensions += get_settings().bad_extensions.extra
    return filename.split('.')[-1] not in bad_extensions


def sort_files_by_main_languages(languages: Dict[str, int], files: List[FileType]) -> List[LanguageGroup]:
    """按主要语言对文件进行分类
    
    Args:
        languages: 语言使用统计字典
        files: 需要分类的文件列表
    Returns:
        按语言分组的文件列表
    """
    if not languages:
        return [LanguageGroup(language="Other", files=filter_bad_extensions(files))]
    
    # 获取语言扩展名映射
    settings = get_settings()
    language_map = {k.lower(): v for k, v in settings.language_extension_map_org.items()}
    
    # 按语言使用量排序
    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    
    # 创建扩展名到语言的映射
    ext_to_lang = {}
    all_main_extensions = set()
    for lang, _ in sorted_languages:
        if lang.lower() in language_map:
            for ext in language_map[lang.lower()]:
                ext_to_lang[ext] = lang
                all_main_extensions.add(ext)
    
    # 对文件进行分类
    lang_groups = defaultdict(list)
    other_files = []
    
    for file in filter_bad_extensions(files):
        if not file.filename:
            continue
        ext = f".{file.filename.split('.')[-1]}"
        if ext in ext_to_lang:
            lang_groups[ext_to_lang[ext]].append(file)
        elif ext not in all_main_extensions:
            other_files.append(file)
    
    # 构建结果
    result = [
        LanguageGroup(language=lang, files=lang_groups[lang])
        for lang, _ in sorted_languages
        if lang_groups[lang]
    ]
    if other_files:
        result.append(LanguageGroup(language="Other", files=other_files))
    
    return result
