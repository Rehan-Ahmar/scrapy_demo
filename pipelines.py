import json
from scrapy.exporters import JsonItemExporter, PprintItemExporter, JsonLinesItemExporter

class ItemPipeline(object):
    def open_spider(self, spider):
        output_json_path = spider.settings.get('OUTPUT_JSON_PATH')
        self.file = open(output_json_path, 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

