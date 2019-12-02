Colin The Computer API Reference
=================================

This is Colin The Computers's API reference.

Thought
---

.. class:: colin.Thought

	Represents a thought, which is defined by a user, a timestamp and the thought itself.

	.. method:: serialize()

		Returns ``bytes`` represeting the thought

	.. classmethod:: deserialize(data)

		Returns Thought object built from ``data``