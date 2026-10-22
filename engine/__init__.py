"""
Módulo de Inicialização do Motor Especialista de Carreiras em TI.
Aplica patch de compatibilidade para a biblioteca Experta em versões modernas do Python (3.10+).
"""
import collections
import collections.abc

# Patch para coleções abstratas movidas para collections.abc no Python 3.10+
_COMPAT_ATTRS = [
    'Mapping',
    'MutableMapping',
    'Sequence',
    'MutableSequence',
    'Iterable',
    'Callable',
    'Container',
    'Hashable',
    'Sized',
    'Set',
    'MutableSet'
]

for _attr in _COMPAT_ATTRS:
    if not hasattr(collections, _attr) and hasattr(collections.abc, _attr):
        setattr(collections, _attr, getattr(collections.abc, _attr))

from engine.facts import (
    UserProfile,
    TrackScore,
    TrackEvaluation,
    FinalRecommendation,
    RuleFiring
)
from engine.advisor import CareerAdvisor

__all__ = [
    'UserProfile',
    'TrackScore',
    'TrackEvaluation',
    'FinalRecommendation',
    'RuleFiring',
    'CareerAdvisor'
]
