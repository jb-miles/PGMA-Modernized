#!/usr/bin/env python
# encoding=utf8
"""
ProviderRegistry - Provider Management
Phase 1: IAFD Removal and Provider Framework

Centralized registry for enrichment providers. Singleton pattern ensures
only one registry instance. Phase 1 supports single provider (IAFDStub).
Phase 3 will extend to multi-provider fallback chains.
"""


class ProviderRegistry(object):
    """
    Singleton registry for metadata enrichment providers.

    Manages provider registration and enrichment requests. All provider
    access goes through this registry to enable future features like
    provider chaining and capability checking.

    Phase 1 Features:
    - Single provider storage
    - Simple error handling
    - Logging integration
    - Statistics tracking (indirectly via provider.get_stats())

    Phase 3 Extensions:
    - Multi-provider fallback chains
    - Priority-based provider selection
    - Provider capability checking
    - Automatic provider switching
    """

    _instance = None
    _provider = None
    _logger = None

    def __new__(cls):
        """Enforce singleton pattern - only one registry instance per process."""
        if cls._instance is None:
            cls._instance = super(ProviderRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, provider, logger=None):
        """
        Initialize the registry with a provider.

        Should be called once at application startup. Subsequent calls
        are ignored if provider already initialized.

        Args:
            provider (DataProvider): Provider instance implementing DataProvider interface
            logger (function): Optional logging function. Expected signature: log(message)
                If None, logging is disabled.
        """
        cls._provider = provider
        cls._logger = logger if logger else lambda x: None
        cls._log('ProviderRegistry initialized with: {0}'.format(
            provider.get_provider_name()
        ))

    @classmethod
    def get_enrichment_cast(cls, name, filmdict):
        """
        Get cast member enrichment data from provider.

        Args:
            name (str): Cast member name
            filmdict (dict): Film context

        Returns:
            dict or None: Cast member data, or None if not found/not available
        """
        if cls._provider is None:
            cls._log('ERROR: ProviderRegistry not initialized')
            return None

        try:
            result = cls._provider.search_cast_member(name, filmdict)
            if result:
                cls._log('Cast enrichment found: {0}'.format(name))
            return result
        except Exception as e:
            cls._log('Provider error (cast {0}): {1}'.format(name, e))
            return None

    @classmethod
    def get_enrichment_director(cls, name, filmdict):
        """
        Get director enrichment data from provider.

        Args:
            name (str): Director name
            filmdict (dict): Film context

        Returns:
            dict or None: Director data, or None if not found/not available
        """
        if cls._provider is None:
            cls._log('ERROR: ProviderRegistry not initialized')
            return None

        try:
            result = cls._provider.search_director(name, filmdict)
            if result:
                cls._log('Director enrichment found: {0}'.format(name))
            return result
        except Exception as e:
            cls._log('Provider error (director {0}): {1}'.format(name, e))
            return None

    @classmethod
    def get_enrichment_film(cls, title, year, studio):
        """
        Get film enrichment data from provider.

        Args:
            title (str): Film title
            year (str): Release year
            studio (str): Studio name

        Returns:
            dict or None: Film data, or None if not found/not available
        """
        if cls._provider is None:
            cls._log('ERROR: ProviderRegistry not initialized')
            return None

        try:
            result = cls._provider.search_film(title, year, studio)
            if result:
                cls._log('Film enrichment found: {0}'.format(title))
            return result
        except Exception as e:
            cls._log('Provider error (film {0}): {1}'.format(title, e))
            return None

    @classmethod
    def get_provider(cls):
        """
        Get current provider instance.

        Returns:
            DataProvider or None: Current provider, or None if not initialized
        """
        return cls._provider

    @classmethod
    def get_provider_stats(cls):
        """
        Get statistics from current provider.

        Returns:
            dict or None: Provider statistics (if available), or None

        Phase 1: Returns IAFDStub call counts
        Phase 3: Will aggregate stats from provider chain
        """
        if cls._provider is None:
            return None

        if hasattr(cls._provider, 'get_stats'):
            return cls._provider.get_stats()

        return None

    @classmethod
    def _log(cls, message):
        """
        Internal logging method.

        Args:
            message (str): Message to log
        """
        if cls._logger:
            cls._logger(message)

    @classmethod
    def reset(cls):
        """
        Reset registry to uninitialized state.

        Used for testing only. In production, should not be called
        after initialization.
        """
        cls._provider = None
        cls._logger = None
