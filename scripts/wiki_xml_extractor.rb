require 'rubygems'
require 'nokogiri'

# This program dumpxml2wiki reads mediawiki xml files dumped by dumpBackup.php
# on the current directory and transforms them into wiki files which can then
# be modified and uploaded again by pywikipediabot using pagefromfile.py on a mediawiki family site.
# The text of each page is searched with xpath and its title is added on the first line as
# an html comment: this is required by pagefromfile.py.
#
Dir.glob("../data/dewiki-latest-pages-articles*").each do |filename|
  input = Nokogiri::XML(File.new(filename), nil, 'UTF-8')

  puts filename.to_s  # prints the name of each .xml file

  File.open("out_" + filename + ".wiki", 'w') {|f|
    input.xpath("//xmlns:text").each {|n|
      pptitle = n.parent.parent.at_css "title" # searching for the title
      title = pptitle.content
      f.puts "\n{{-start-}}<!--'''" << title.to_s << "'''-->" << n.content  << "\n{{-stop-}}"
    }
  }
end

#### this part cleans the extracted text. Script is in progress

file_content = File.open("out_dewiki-latest-pages-articles1.xml-p000000001p000425449.wiki", "r:UTF-8", &:read); nil
file_content = file_content.gsub(/\n/, ""); nil
content = []
file_content.scan(/{{-start-}}(.*?){{-stop-}}/).each do |hit|
  content << hit.to_s
end; nil

File.open("test", "w+") do |f|
  content.each { |element| f.puts(element) }
end; nil


categories = []
File.readlines('gesundheit_category.txt').each do |line|
  line = line.gsub(/\n/, "")
  categories << line
end; nil

matches = []

content.each do |element|
  catch :categoryfound do
    categories.each do |category|
      if element.include?("[[Kategorie:#{category}]]")
        matches << element
      end
    end
  end
end; nil

matches.map! do |element|
  element = element.gsub(/<ref(.*?)<\/ref>/, "")
  element = element.gsub(/== Literatur ==(.*?)==/, "")
  element = element.gsub(/== Weblinks ==(.*?)==/, "")
  element = element.gsub(/== Einzelnachweise ==(.*?)==/, "")
  element = element.gsub(/\[\[/, "")
  element = element.gsub(/\]\]/, "")
  element = element.gsub(/<ref(.*?)>/, "")
  element = element.gsub(/\'\'{{lang(.*?)\'\'/, "")
  element = element.gsub(/{{lang(.*?)}}/, "")
  element = element.gsub(/=====/, "")
  element = element.gsub(/====/, "")
  element = element.gsub(/===/, "")
  element = element.gsub(/==/, "")
  element = element.gsub(/'''''/, "")
  element = element.gsub(/''''/, "")
  element = element.gsub(/'''/, "")
  element = element.gsub(/''/, "")
  element = element.gsub(/\*\*\*\*\*/, "")
  element = element.gsub(/\*\*\*\*/, "")
  element = element.gsub(/\*\*\*/, "")
  element = element.gsub(/\*\*/, "")
  element = element.gsub(/\{\|(.*?)\|\}/, "")
  element = element.gsub(/\{\{(.*?)\}\}/, "")
  element = element.gsub(/&nbsp\;/, "")
end;nil
