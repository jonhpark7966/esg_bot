from abc import ABC, abstractmethod

class ReportHandler(ABC):
    def __init__(self, company_name, year, report_url):
        """
        Initialize the class with attributes.

        Parameters:
        companay_name (string): companay name
        year (int): year of report
        reprot_url (string): web url to wget (might be a s3 url for pdf file).
        """
        self.compnay_name = company_name
        self.year = year
        self.report_url = report_url

    @abstractmethod
    def splitReport(self, save_dir, report_name):
        """
        Abstract function
        Split or extract components of report.
        ex.  PDF file -> text, table, image compenents

        Returns:
        dictionary: dict contans the component type names and components.
        """
        pass