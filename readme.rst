NaviCore Dashboard
==================

A web page to show Jenkins job status and Google Test results.

.. warning:: It's a Work-in-Progress. Please use it at your own risk.

We put it on a screen near the entrance of our work area.
So if something goes wrong, anyone passes by will notice it.
We have been relying on it for some years. And we plan to improve it in the later half of 2019.

.. image:: docs/images/live_image.jpg

Features
--------

* Show Jenkins Job status(blue, yellow, red).
* Show the name of failed tests.

Planing Features
----------------

* Adaptive layout for both small and large screens.
* Read data from XML output of GoogleTest.
* Hierarchical display. (Click to show more details. Jobs -> Test Suites -> Test Cases)
* Timeline. Show the status history so that you can see when the job failed and when it recovered.
