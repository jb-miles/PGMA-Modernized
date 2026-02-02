#!/usr/bin/env python
# encoding=utf8
"""
DataProvider Abstract Base Class
Phase 1: IAFD Removal and Provider Framework

Defines the standard interface for all metadata enrichment providers.
Future providers (GEVI, WayBig, AEBN, etc.) will implement this interface.
"""

from abc import ABCMeta, abstractmethod


class DataProvider(object):
    """
    Abstract base class for metadata enrichment providers.

    Defines standard interface for cast, director, and film enrichment.
    All providers must implement these methods.

    Phase 1: IAFDStub implements this interface, returning None for all calls.
    Phase 3: GEVIProvider and WayBigProvider will implement real lookups.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def search_cast_member(self, name, filmdict):
        """
        Search for cast member by name.

        Args:
            name (str): Cast member name to search for
            filmdict (dict): Film context dictionary with keys:
                - 'Title': Film title
                - 'Year': Release year (str)
                - 'Studio': Studio name

        Returns:
            dict: Cast member data with keys (if found):
                - 'RealName': str or None - Legal name of performer
                - 'Alias': str - Screen name or alias (defaults to original name)
                - 'Photo': str URL or None - Profile photo URL
                - 'URL': str or None - Link to performer profile
                - 'Bio': dict - Biographical data (details depend on provider)
                - 'Nationality': str or None - Country/nationality
                - 'Awards': list of str - Award names
                - 'Films': list of str - Film appearances
                - 'Role': str - Character role (usually empty string)

            None: If no match found or search not supported
        """
        pass

    @abstractmethod
    def search_director(self, name, filmdict):
        """
        Search for director by name.

        Args:
            name (str): Director name to search for
            filmdict (dict): Film context dictionary

        Returns:
            dict: Director data (same structure as cast member)
            None: If no match found or search not supported
        """
        pass

    @abstractmethod
    def search_film(self, title, year, studio):
        """
        Search for film by title, year, and studio.

        Args:
            title (str): Film title
            year (str): Release year
            studio (str): Studio name

        Returns:
            dict: Film data with keys (if found):
                - 'Cast': dict - Cast members {name: castdict}
                - 'Directors': dict - Directors {name: directordict}
                - 'ReleaseDate': datetime or None - Release date
                - 'Duration': datetime or None - Film duration
                - 'Countries': set - Countries of origin

            None: If no match found or search not supported
        """
        pass

    def get_provider_name(self):
        """
        Return provider name for logging purposes.

        Returns:
            str: Name of this provider (e.g., 'IAFDStub', 'GEVIProvider')
        """
        return self.__class__.__name__
