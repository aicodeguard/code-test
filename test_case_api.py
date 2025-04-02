import base64
import json
import os
import uuid
from fastapi import APIRouter, HTTPException

from api.test_case_model import UpdateStepsRequest, GenerateTestStepsRequest
from config.init_conf import TEST_CASE_FILE
from service.generate_test_case import get_element, get_cases
from service.generate_yaml import generate_yaml
from service.ui_automation import invoke_midscenejs

from fastapi.logger import logger

from utils.mock_data_util import get_mock_test_cases, get_get_case_by_id
from utils.path_util import get_cookies_path, get_data_path

router = APIRouter()

@router.post("/api/test-cases/{test_case_id}/steps")
async def update_test_case_steps(test_case_id: str, request: UpdateStepsRequest):
    try:
        # Load test cases from JSON file
        json_file_path = os.path.join(get_data_path(), TEST_CASE_FILE)
        with open(json_file_path, 'r') as file:
            test_cases_data = json.load(file)

        # Find the test case by ID and update the steps
        test_case = next((tc for tc in test_cases_data['test_cases'] if tc['id'] == test_case_id), None)

        if not test_case:
            raise HTTPException(
                status_code=404,
                detail=f"Test case {test_case_id} not found"
            )

        logger.error("Test case {request.steps} found", request.steps)

        # 修改: 将 TestStep 对象列表转换为字典列表
        test_case['steps'] = [step.dict() for step in request.steps]

        # Save the updated test cases back to the JSON file
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(test_cases_data, file, indent=4, ensure_ascii=False)

        return {
            "status": "success",
            "message": f"Steps updated for test case {test_case_id}",
            "data": {
                "test_case_id": test_case_id,
                "steps": request.steps
            }
        }
    except Exception as e:
        logger.error(f"Error running test case {test_case_id}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update test case steps: {str(e)}"
        )


@router.get("/api/test-cases")
async def get_all_test_cases():
    try:
        # TODO: 这里暂时把数据放到了json文件中，需要调整到数据库
        test_cases = get_mock_test_cases()
        return {
            "status": "success",
            "data": {
                "test_cases": test_cases,
                "total": len(test_cases)
            }
        }
    except Exception as e:
        logger.error(f"Error running /api/test-cases", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve test cases: {str(e)}"
        )

# 新增接口：创建测试用例
@router.post("/api/test-cases/create")
def create_test_case(request: GenerateTestStepsRequest):
    try:
        # 获取请求中的 description、url 和 createdAt
        description = request.description
        url = request.url
        created_at = request.createdAt

        # 打开cookie文件读取cookie
        cookies = []
        with open(get_cookies_path(), 'r') as f:
            cookies = json.load(f)
        element_html = get_element(cookies, url)
        tmp_this_cases = get_cases(element_html, base64.b64encode(open('a.png', "rb").read()).decode('utf-8'), description)
        logger.info(tmp_this_cases)

        # 加载现有的测试用例数据
        json_file_path = os.path.join(get_data_path(), 'test_cases.json')
        with open(json_file_path, 'r') as file:
            test_cases_data = json.load(file)

        # 如果tmp_this_cases不为空，则遍历tmp_this_cases，按照下列格式生成多个test_case并保存进json文件中
        if tmp_this_cases:
            for case in tmp_this_cases:
                # 构造每个测试用例数据
                test_case = {
                    "id": f"tc-{str(uuid.uuid4())[:8]}",  # 自动生成 ID
                    "description": description,
                    "url": url,
                    "createdAt": created_at,
                    "yaml_path": "",
                    "result_url": "",
                    "status": "pending",  # 初始状态为 pending
                    "steps": case['steps'],  # 根据当前case的内容填充步骤
                }

                # 将新测试用例添加到数据中
                test_cases_data.setdefault("test_cases", []).append(test_case)
        else:
            # 如果tmp_this_cases为空，则构建一个空的test_case，并保存进json文件中
            empty_test_case = {
                "id": f"tc-{str(uuid.uuid4())[:8]}",  # 自动生成 ID
                "description": description,
                "url": url,
                "createdAt": created_at,
                "yaml_path": "",
                "result_url": "",
                "status": "pending",  # 初始状态为 pending
                "steps": [],  # 空步骤
            }

            # 将空测试用例添加到数据中
            test_cases_data.setdefault("test_cases", []).append(empty_test_case)

        # 保存更新后的测试用例数据到json文件中
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(test_cases_data, file, indent=4, ensure_ascii=False)
        return {
            "status": "success",
            "message": "Test case created successfully.",
            "data": []
        }

    except Exception as e:
        logger.error(f"Error creating test case", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create test case: {str(e)}"
        )

# 新增接口：运行测试用例
@router.post("/api/test-cases/{test_case_id}/run")
async def run_test_case(test_case_id: str):
    try:
        # Find the test case by ID
        test_case = get_get_case_by_id(test_case_id)
        if not test_case:
            raise HTTPException(
                status_code=404,
                detail=f"Test case {test_case_id} not found"
            )
        steps = test_case['steps']
        yaml_name = test_case["id"] + ".yaml"
        output_path = os.path.join(get_data_path(), yaml_name)
        if not os.path.exists(output_path):
            template_path = os.path.join(get_data_path(),
                                     "test_case_template.yaml")
            generate_yaml(test_case, steps, template_path, output_path)


        ui_result = invoke_midscenejs(output_path)
        logger.info(ui_result)

        # Simulate running the test case (for demonstration purposes)
        # In a real-world scenario, you would execute the steps here
        result = {
            "status": "success",
            "message": f"Test case {test_case_id} executed successfully",
            "data": {
                "test_case_id": test_case_id,
                "steps": steps
            }
        }

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run test case {test_case_id}: {str(e)}"
        )
