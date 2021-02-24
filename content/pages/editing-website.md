Title: Editing this Website
URL: editing-website.html
save_as: editing-website.html
template: page

# Editing this Website

This website is hosted in its own git repository `solr-site` (see [Github](https://github.com/apache/solr-site/) and [Gitbox](https://gitbox.apache.org/repos/asf/solr-site.git)).

The content of the `main` branch will update the [staging site](https://solr.staged.apache.org) while the content of the `production` branch will be published to the main website. Read the [README.md](https://github.com/apache/solr-site/) file for further instructions.

## Contributing content

If you want to contribute some content or bugfix to this website, you may follow these steps:

1. Fork this repository in [GitHub](https://github.com/apache/solr-site)
2. Clone your fork to your computer

        git clone https://github.com/<your-github-id>/lucene-site
        cd lucene-site
        git pull

3. Create a new branch for your edits

        git checkout -b my-typo-fix

4. Edit the site following the instructions in [README](https://github.com/apache/solr-site/)
5. When done, push your changes to your branch (in your fork)

        git add .
        git commit -m "Fixing a typo on the resources page"
        git push origin

6. Visit your fork again on GitHub, and you'll se a button to add your branch as a Pull Request

For more detailed instructions, see [GitHub documentation](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork).

**TIP:** For very simple edits to one page only, you may find the page (markdown or html) in GitHub, then click the edit button and submit your PR directly from the UI.
