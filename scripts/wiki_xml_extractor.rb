require 'rubygems'
require 'nokogiri'

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

input = Nokogiri::XML(File.new(filename), nil, 'UTF-8')
input.xpath("//xmlns:text").each do |n|
  pptitle = n.parent.parent.at_css "title" # searching for the title
  title = pptitle.content.to_s
  content = n.content

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