import time
import yaml

# should be called from the root dir
my_name = "Tianji Liu"
website_url = "https://tefantasy.github.io/"
citation_meta_dir = "docs/"

def gen_citation_meta(pub):
    # find PDF file path
    pdf_path, pdf_name = None, None
    if "links" in pub:
        for text, link in pub["links"]:
            if text == "paper" and not link.startswith("https:"):
                pdf_path = website_url + link
                pdf_name = link.split("/")[-1].split(".")[0]
                break
    if pdf_path is None:
        print("Generate citation meta failed for paper: %s" % pub["title"])
        exit(1)

    html = "<!DOCTYPE html>\n<html>\n<head>\n"
    html += "<title>Paper Meta</title>\n"

    # meta tags
    html += '<meta name="citation_title" content="%s">\n' % pub["title"]
    authors = [author.strip().replace("*", "") for author in pub["authors"].split(",")]
    for author in authors:
        html += '<meta name="citation_author" content="%s">\n' % author
    html += '<meta name="citation_publication_date" content="%d">\n' % pub["year"]
    html += '<meta name="citation_pdf_url" content="%s">\n' % pdf_path

    # other info
    html += "</head>\n<body>\n"
    html += "<p>Meta data for %s</p>\n" % pub["title"]
    html += "</body>\n</html>\n"

    citation_meta_path = citation_meta_dir + "%s_meta.html" % pdf_name
    with open(citation_meta_path, "w") as f:
        f.write(html)
    return citation_meta_path

def gen_pubs(pubs):
    html = ""
    meta_pathes = {}
    bold_my_name = "<b>" + my_name + "</b>"

    # show in reversed order
    for pub in reversed(pubs):
        html += "<li>\n"

        assert "authors" in pub
        assert my_name in pub["authors"]
        html += pub["authors"].replace(my_name, bold_my_name) + ", "

        assert "title" in pub
        html += '"' + pub["title"] + '", '

        assert "conf" in pub or "jour" in pub
        conf_jour = pub["conf"] if "conf" in pub else pub["jour"]
        html += conf_jour + " "

        assert "abbr" in pub
        html += "(<b>" + pub["abbr"] + "</b>), "

        assert "year" in pub
        html += str(pub["year"]) + ". "

        if "other_info" in pub:
            html += pub["other_info"] + " "
        
        if "links" in pub:
            for text, link in pub["links"]:
                html += '[<a href="%s" target="_blank">%s</a>] ' % (link, text)

        if "citation_meta" in pub and pub["citation_meta"]:
            citation_meta_path = gen_citation_meta(pub)
            html += '<a href="%s" style="display:none;">Metadata</a>' % citation_meta_path
            meta_pathes[pub["title"]] = citation_meta_path
        
        html += "\n</li>\n"
    return html, meta_pathes

def gen_awards(awards):
    html = ""

    # show in reversed order
    for award in reversed(awards):
        html += "<li>\n"

        assert "award" in award
        html += award["award"] + ", "

        assert "year" in award
        html += str(award["year"]) + ". "

        if "other_info" in award:
            html += award["other_info"] + " "
        
        html += "\n</li>\n"
    return html


def gen_sitemap(pubs, meta_pathes):
    block_templ = '<url>\n<loc>%s</loc>\n<priority>%s</priority>\n</url>\n\n'

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n'

    sitemap += block_templ % (website_url, "1.00")
    
    for pub in reversed(pubs):
        if "links" not in pub:
            continue
        
        for _, link in pub["links"]:
            if link.startswith("https:"):
                continue
            full_link = website_url + link
            sitemap += block_templ % (full_link, "0.80")
        
        if pub["title"] in meta_pathes:
            meta_path = website_url + meta_pathes[pub["title"]]
            sitemap += block_templ % (meta_path, "0.80")

    sitemap += "</urlset>\n"

    return sitemap

# load HTML template
with open("index.html.tmpl", "r") as f:
    html_template = f.read()

# load pubs and awards
with open("res/pubs.yaml", "r") as f:
    pubs = yaml.safe_load(f)
with open("res/awards.yaml", "r") as f:
    awards = yaml.safe_load(f)

pubs_html, meta_pathes = gen_pubs(pubs)
awards_html = gen_awards(awards)

index_html = html_template.replace("__PUBS__", pubs_html).replace("__AWARDS__", awards_html)

# update time
index_html = index_html.replace("__UPDATE_TIME__", time.strftime("%b %d, %Y", time.localtime()))

with open("index.html", "w") as f:
    f.write(index_html)

# generate sitemap
sitemap_xml = gen_sitemap(pubs, meta_pathes)
with open("res/sitemap.xml", "w") as f:
    f.write(sitemap_xml)
