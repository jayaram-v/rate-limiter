# Plan
    Read this file and agents.md to understand system requirements, technical requests. Change and improve this file, plan.md for this purpose. 

# Rate limiter strategy
    Analyse and come up with rate limiter strategy for this requirement. Give multiple options and give tradeoffs. Do not implement anything until a strategy is selected.

# Folder and File Structure 
    Come up with the scaffolding for this project.Tentatively this is ,
    config.yaml
    project.yaml
    src/
    scripts/
    test/
    doc/
    backend/
    requirements.txt
    readme.md

# Data Model
    Come up with the data model for this requirement. Create a simple cache for this project.

    Request key
    - user id or source ip
    - endpoint id
    - request time
    - port
    - status

# Technical structure
    Come up with technical scaffolding for docker, FastAPI and pydantic. Create runnable scripts to test the application at folder test/

# Test Plan
    Create a test plan and test with pytest for two functionalities - rate_limiter_api and cache_read.

    Come up with more test cases and plans as necessary. Follow the test case format ,

    Test_case_id    test_case_name  test_case_description    Requirement_description    Module  File_name    Pass/Fail  Expected    Actual
    1   SAMPLE  SAMPLE_DESC SAMPLE_REQ  __init__    __init__.py PASS    1   1

# MVP
    Create an MVP first with basic implementation to check whether the rate_limiter component works before working on other aspects of the project.
