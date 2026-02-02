#!/usr/bin/env python
# encoding=utf8
"""
IAFDStub - Graceful No-Op Enrichment Provider
Phase 1: IAFD Removal and Provider Framework

This stub provides graceful degradation while IAFD is unavailable due to
HTTP 403 blocking. Returns None for all enrichment requests while logging
activity for monitoring and Phase 3 planning.
"""

from DataProvider import DataProvider


class IAFDStub(DataProvider):
    """
    Stub implementation of DataProvider.

    Gracefully returns None for all enrichment requests. Logs all attempts
    to aid debugging and planning. Tracks statistics on requested enrichment.

    Phase 1 Usage:
    - All agents use this stub instead of IAFD
    - Search/match rates unchanged (stub returns None, agents degrade gracefully)
    - Enrichment rate: 0% (expected - stub returns None)
    - Side benefit: Performance improvement (no IAFD timeout waits)

    Phase 3:
    - Will be replaced by GEVIProvider as primary
    - Statistics from this stub will inform Phase 3 provider selection
    """

    def __init__(self, logger=None):
        """
        Initialize IAFDStub.

        Args:
            logger (function): Optional logging function. If not provided,
                uses simple print() to stderr. Expected signature: log(message)
        """
        self.logger = logger if logger else self._default_log
        self._call_count = {
            'cast': 0,
            'director': 0,
            'film': 0
        }

    def _default_log(self, message):
        """Default logger using print if none provided."""
        print('IAFDStub :: {0}'.format(message))

    def search_cast_member(self, name, filmdict):
        """
        Log cast search request and return None.

        Phase 1: Always returns None. All enrichment requests are logged.
        """
        self._call_count['cast'] += 1
        self.logger('IAFD unavailable - cast search for: {0} (Film: {1})'.format(
            name,
            filmdict.get('Title', 'Unknown')
        ))
        return None

    def search_director(self, name, filmdict):
        """
        Log director search request and return None.

        Phase 1: Always returns None. All enrichment requests are logged.
        """
        self._call_count['director'] += 1
        self.logger('IAFD unavailable - director search for: {0} (Film: {1})'.format(
            name,
            filmdict.get('Title', 'Unknown')
        ))
        return None

    def search_film(self, title, year, studio):
        """
        Log film search request and return None.

        Phase 1: Always returns None. All enrichment requests are logged.
        """
        self._call_count['film'] += 1
        self.logger('IAFD unavailable - film search for: {0} ({1}) - Studio: {2}'.format(
            title,
            year,
            studio
        ))
        return None

    def get_stats(self):
        """
        Get usage statistics for this stub.

        Returns:
            dict: Call counts by type
                - 'cast': Number of cast enrichment requests
                - 'director': Number of director enrichment requests
                - 'film': Number of film enrichment requests
        """
        return self._call_count.copy()

    def get_total_requests(self):
        """
        Get total number of enrichment requests attempted via this stub.

        Returns:
            int: Sum of all enrichment requests
        """
        return sum(self._call_count.values())
