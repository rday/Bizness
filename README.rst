Purpose
============

There are a lot of introductory programming resources available. There are a lot of advanced
programming resources available as well. But the in-between is a really tough area. You are
either introducing new concepts, which can be a bit trivial or boring (a lot of people have
already read the webpage). Or you need very tough, specific, real world circumstances which
involve a lot of context that doesn't apply to many people's needs.

So why not build a simple application from the ground up, using trivial straight forward
concepts. At the same time ramble on about the more advanced ideas you might encounter in
the future. Plan for those ideas in this simple application.

Ideally the problem domain will never interfere with understanding the technical challenges.
This makes it easy to focus on techniques without getting drowned in details.


Premature Optimization
======================

Prevailing wisdom tells us not to optimize our applications prematurely. While this is
correct, it falls into one of those arguable contextual problems we all see when theory
hits reality. Just because our site isn't in production doesn't mean we can use a weak
password hash. Even though we don't have any data, we should still think a little about
our database indexes and relationships.

There are a few items we will assume to be true for this application. We will focus on
these items early on:

* We want to have multiple developers on a project
* We want to test our code
* We want to effectively find and fix bugs. Proactively when possible.

With these assumptions in mind, we will be focusing on aspects of development which
may not seem appropriate given the state of the application.


First Iteration
===============

The goal for these iterations is not to simply build another demo Flask application.
The goal is to establish good development habits for larger projects.

In the first iteration we have a very simple business application. So simple, in fact,
that it won't even run. When we import our config file, it doesn't exist. Keeping
the configuration file out of source control is very important for security. Config
files have things like API keys and database passwords in them. When bringing on new
developers, or if you project is public, you don't need to release your secret keys to
the world.

We will keep a template version of our config file. This will give new developers something
to copy locally, while keeping our secrets hidden.


Second Iteration
================

This iteration we add a simple database. It uses SQLite and only has one table. Still, we've
got an alembic migration script. By using alembic to document the creation of the database
in source control, we will be able to rebuild the database without issue when we add our
production database.