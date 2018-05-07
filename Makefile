
test:
	pytest --html=pytest/report.html --self-contained-html --junit-xml=pytest/junit.xml --cov=pymycity/ --cov-report=term --cov-report=html:pytest/coverage/html --cov-report=xml:pytest/coverage/coverage.xml -p no:pytest_wampy tests 

