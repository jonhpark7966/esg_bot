from abc import ABC, abstractmethod

class SummaryHandler(ABC):
    @abstractmethod
    def summary(self, components):
        """
        Abstract function
        get splitted pdf components and make summary of each components

        Returns:
        dictionary: dict contans the component type names and components.
        """
        pass
