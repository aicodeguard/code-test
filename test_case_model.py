#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 File Name: test_case_model、
 Description:
 Author: Allen
 Created Time: 2025/3/31 11:17
"""
from typing import Optional, List

from pydantic import BaseModel


class TestStep(BaseModel):
    description: str
    action: Optional[str] = "click"
    selector: Optional[str] = ""
    value: Optional[str] = ""


class UpdateStepsRequest(BaseModel):
    steps: List[TestStep]


class GenerateTestStepsRequest(BaseModel):
    description: str
    url: str
    createdAt: str


class TestCase(BaseModel):
    id: str
    description: str
    url: str
    createdAt: str
    steps: List[TestStep]
