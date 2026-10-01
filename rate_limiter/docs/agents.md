# Requirements
1. The main requirement is rate limiter service to limit middleware from accessing an HTTP API endpoint.
2. The service should have a way to configure limit for 10 concurrent users accessing from certain IPs and ports with access to an endpoint. 
3. We also need an ability for admin users to bypass the rate limiter.

# Technical spec
1. Use Python (>=3.12) for the entire system
2. Any in memory cache to store user data (around 10 to test) and to have base configuration for users
3. Two python services created to simulate requesting system and endpoint HTTP.
4. Feel free to use PIP. 
5. All code must follow SOLID
6. Use two YAML files for system level configurations - config.yaml, project.yaml
7. Create test scripts to test using pytest and create wrapper scripts and documentation for manual testing by developer.
8. Expose one API for accessing the rate limiter from the service with FastAPI and check all data types with Pydantic. 
9. IP list should be configurable via cache and YAML.

# Limitations
1. Keep the cache data model simple with less than 15 samples for user info
2. Keep the tests simple with documentation for manual tests and create a test plan in /test
3. Only one rate limiter service with 2 test services to test the source request and endpoint.

