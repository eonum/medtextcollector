require 'rubygems'
# gem install libxml-ruby
require 'xml'
require 'digest'

wiki_dump_file = ARGV[0]
wiki_output_folder = ARGV[1]
categories_file = ARGV[2]

def clean_and_write_article file_prefix, content
  content = content.gsub(/<ref(.*?)<\/ref>/m, " ")
  content = content.gsub(/== Literatur ==(.*?)==/, " ")
  content = content.gsub(/== Weblinks ==(.*?)==/, " ")
  content = content.gsub(/== Einzelnachweise ==(.*?)==/, " ")
  content = content.gsub(/ Einzelnachweise (.*?)\n/, " ")
  content = content.gsub(/<!--(.*?)-->/m, " ")
  content = content.gsub(/Kategorie(.*?)\n/, " ")
  content = content.gsub(/ Datei:(.*?)\n/, " ")
  content = content.gsub(/:{(.*?)}/m, " ")
  content = content.gsub(/#REDIRECT(.*?)\n/, " ")
  content = content.gsub(/\[\[/, " ")
  content = content.gsub(/\]\]/, " ")
  content = content.gsub(/<ref(.*?)>/m, " ")
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
  content = content.gsub(/\{\|(.*?)\|\}/m, " ")
  content = content.gsub(/\{\{(.*?)\}\}/m, " ")
  content = content.gsub(/&nbsp\;/, " ")

  content = content.strip
  return false if content == ''

  filename = file_prefix + "#{Digest::MD5.hexdigest(content)}"
  return false if File.exist?(filename)

  File.open(filename, "w") do |f|
    f.write content
  end

  return true
end

# This program dumpxml2wiki reads mediawiki xml file and transforms them into wiki files.

categories = []
File.readlines(categories_file).each do |line|
  line = line.gsub(/\n/, "")
  categories << line
end

counter = 0
negative_counter = 0

docstream = XML::Reader.file wiki_dump_file
while docstream.read
  if (docstream.name == 'text')
    docstream.read
    content = docstream.value
    found_category = false
    categories.each do |category|
      if content.include?("[[Kategorie:#{category}]]")
        # category found
        found_category = true
        counter += 1 if clean_and_write_article wiki_output_folder + "/positive/clean_extract_", content

        if (counter % 10 == 0)
          puts "Processing matched article nr. " + counter.to_s
        end
      end
    end

    if not found_category
      if negative_counter < counter
        negative_counter += 1 if clean_and_write_article wiki_output_folder + "/negative/clean_extract_", content
      end
    end
  end
end
