``ayni``
========
A webservice with three different components to aid in proper documentation
ordering:

#. An HTTP API that serves JSON pointing to the various different versions of
   documentation available and its URLs.

#. A dynamically generated Nginx file that maps URLs to the proper (current)
   versions of a project(s) documentation.

#. A JavaScript library that should be injected into the Sphinx theme that
   understands how to talk to the exposed HTTP API and display a navigation
   menu to move to different documentation versions.
