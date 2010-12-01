coverage_report coverage_report_log.txt: $(shell find -name '*.py')
	rm -rf coverage_report
	mkdir -p coverage_report
	PYTHONPATH=. COVERAGE_REPORT_HTML_OUTPUT_DIR="$(CURDIR)/coverage_report" python test_project/manage.py test_coverage django_testscenarios -v0 2>&1 | tee coverage_report_log.txt

on_commit:: coverage_report
	rsync -a coverage_report zero-kelvin.pl:/var/www/www.zero-kelvin.pl/django_testscenarios/

clean:
	rm -rf coverage_report
	rm -f coverage_report_log.txt
