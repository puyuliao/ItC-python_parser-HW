from crawler import Crawler
from args import get_args


if __name__ == '__main__':
    args = get_args()  
    crawler = Crawler()
    contents = crawler.crawl(args.start_date, args.end_date)
    # TODO: write content to file according to spec
    with open(args.output,'w') as f:
        for date, title,content in contents:
            out_str = f'{str(date)},"{title}","{content}"\n'
            #print(out_str)
            f.write(out_str)
