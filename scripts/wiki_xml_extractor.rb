require 'rubygems'
require 'xml'

wiki_dump_file = ARGV[0]
wiki_output_folder = ARGV[1]
categories_file = ARGV[2]

# This program dumpxml2wiki reads mediawiki xml file and transforms them into wiki files.

categories = []
File.readlines(categories_file).each do |line|
  line = line.gsub(/\n/, "")
  categories << line
end

matched_articles = []

# TODO replace counter with Hash
counter = 0

docstream = XML::Reader.file wiki_dump_file
while docstream.read
  if (docstream.node_type == XML::Reader::TYPE_ELEMENT && docstream.name == 'text')
    if( count %100 == 0)
      puts "Processing matched article nr. " + counter.to_s
    end

    content = docstream.value

    categories.each do |category|
      if article.include?("[[Kategorie:#{category}]]")
        # category found

        content = content.gsub(/<ref(.*?)<\/ref>/, " ")
        content = content.gsub(/== Literatur ==(.*?)==/, " ")
        content = content.gsub(/== Weblinks ==(.*?)==/, " ")
        content = content.gsub(/== Einzelnachweise ==(.*?)==/, " ")
        content = content.gsub(/\[\[/, " ")
        content = content.gsub(/\]\]/, " ")
        content = content.gsub(/<ref(.*?)>/, " ")
        content = content.gsub(/\'\'{{lang(.*?)\'\'/, " ")
        content = content.gsub(/{{lang(.*?)}}/, " ")
        content = content.gsub(/=====/, " ")
        content = content.gsub(/====/, " ")
        content = content.gsub(/===/, " ")
        content = content.gsub(/==/, " ")
        content = content.gsub(/'''''/, " ")
        content = content.gsub(/''''/, " ")
        content = content.gsub(/'''/, " ")
        content = content.gsub(/''/, " ")
        content = content.gsub(/\*\*\*\*\*/, " ")
        content = content.gsub(/\*\*\*\*/, " ")
        content = content.gsub(/\*\*\*/, " ")
        content = content.gsub(/\*\*/, " ")
        content = content.gsub(/\{\|(.*?)\|\}/, " ")
        content = content.gsub(/\{\{(.*?)\}\}/, " ")
        content = content.gsub(/&nbsp\;/, " ")

        File.open(wiki_output_folder + "/clean_extract_" + "#{counter}", "w") do |f|
          f.write title + "\n"
          f.write content
        end

        counter += 1
      end
    end
  end
end