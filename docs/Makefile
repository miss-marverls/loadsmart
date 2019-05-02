# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -c .
SPHINXBUILD   = sphinx-build
SOURCEDIR     = rst/
SOURCEDIR_AUX = rst/custom_made/
BUILDDIR      = _build/

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

clean:
	@echo "Removing rst files..."
	@rm -f $(SOURCEDIR)*.rst
	@$(SPHINXBUILD) -M $@ $(SOURCEDIR) "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
# Force create source files.
	@sphinx-apidoc -f -o $(SOURCEDIR) .. '../*/migrations' '../manage.py'
	@cp $(SOURCEDIR_AUX)/custom_index.rst $(SOURCEDIR)/index.rst
# Build documentation
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)