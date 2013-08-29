import re
import os
import json
import shutil
import datetime

import logbook
import lxml.html
from scrapelib import Scraper
from scrapelib.cache import FileCache
from jinja2 import Environment, FileSystemLoader


import settings

logger = logbook.Logger('platform-update')
env = Environment(loader=FileSystemLoader('templates'))
solution_tmpl = env.get_template('solution.txt')
issue_tmpl = env.get_template('issue.txt')

request_defaults = {
    # 'timeout': 5.0,
    # 'headers': {
    #     'Accept': ('text/html,application/xhtml+xml,application/'
    #                'xml;q=0.9,*/*;q=0.8'),
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'en-us,en;q=0.5',
    #     'Connection': 'keep-alive',
    #     },
    'follow_robots': False,
    }

if settings.DEBUG:
    request_defaults.update({
        # 'requests_per_minute': 0,
        # 'cache_write_only': False,
        # 'cache_obj': FileCache('cache')
        })
session = Scraper(**request_defaults)


def fetch(url):
    logger.info('requests.get: %r' % url)
    resp = session.get(url, verify=False)
    html = resp.text.encode('utf-8')
    doc = lxml.html.fromstring(html)
    doc.make_links_absolute(url)
    return doc

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


def main():

    done = set()

    # Blow away the current build.
    shutil.rmtree('issues')

    # Get the index page.
    url = 'https://kallosforcouncil.com/solutions/all'
    doc = fetch(url)

    # Get each subject page.
    for url in doc.xpath('//a[contains(@href, "/solutions/")]/@href')[4:]:

        if url in done:
            continue

        doc = fetch(url)

        # Get the issue info.
        try:
            issue_name = doc.xpath('//h3/div/a')[0].text_content()
        except IndexError:
            # Probably the empty "other" page. Skip.
            continue
        xpath = '//div[@class="view-summary"]'

        try:
            issue_desc = doc.xpath(xpath).pop().text_content()
        except IndexError:
            # No description. Skip.
            issue_desc = None
        else:
            issue_desc = issue_desc.replace(u'\xa0', ' ')

        # Make the issue folder.
        try:
            os.makedirs('issues/%s/' % issue_name)
        except OSError:
            pass

        # Write the issue md file.
        with open('issues/%s/README.md' % issue_name, 'w') as f:
            md = issue_tmpl.render(
                name=issue_name, description=issue_desc, url=url)
            f.write(md.encode('utf-8'))

        done.add(url)

        # Get each detail page.
        xpath = ('//div[@class="solution-list"]/'
                 'descendant::a[contains(@href, "/solution/")]/@href')
        for detail_url in doc.xpath(xpath):
            if detail_url in done:
                continue
            detail_doc = fetch(detail_url)
            first = lambda xpath: detail_doc.xpath(xpath).pop()
            data = {}
            data['title'] = first('//h1[@class="title"]/text()')

            _, slug = detail_url.rsplit('/', 1)
            submitted = first('//span[@class="submitted"]/text()')
            rgx = r'Submitted by (.+?) on \S+ (.+)(?:am|pm)'
            submitter, subm_str = re.findall(rgx, submitted).pop()
            subm_dt = datetime.datetime.strptime(subm_str, '%m/%d/%Y - %H:%M')
            data.update(submitter=submitter, submitted_datetime=subm_dt)

            upvotes = first('//div[@class="alternate-votes-display"]/text()')
            data['upvotes'] = upvotes

            xpath = '//div[@class="field-items"]'
            for div in detail_doc.xpath(xpath)[:2]:
                key, text = div.text_content().strip().split(None, 1)
                key = key.lower().strip(':')
                data[key] = text

            xpath = (
                '//div[contains(@class, "field-field-solution-explanation")]')
            try:
                _, expl = first(xpath).text_content().split(None, 1)
            except IndexError:
                # Some pages have no explanation. Skip.
                pass
            else:
                data['explanation'] = expl.strip()

            pdf_url = first('//a[contains(@href, "printpdf")]/@href')
            data['pdf_url'] = pdf_url
            data['url'] = detail_url

            # Write the solution md file.
            with open('issues/%s/%s.md' % (issue_name, slug), 'w') as f:
                md = solution_tmpl.render(**data).encode('utf-8')
                f.write(md)

            # Dump the json file.
            with open('issues/%s/%s.json' % (issue_name, slug), 'w') as f:
                json.dump(data, f, cls=DateTimeEncoder, indent=4)

            done.add(detail_url)


if __name__ == '__main__':
    main()
