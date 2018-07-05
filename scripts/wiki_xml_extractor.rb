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
        clean_and_write_article wiki_output_folder + "/positive/clean_extract_", content

        if (counter % 10 == 0)
          puts "Processing matched article nr. " + counter.to_s
        end
        counter += 1
      end
    end

    if not found_category
      if negative_counter < counter
        clean_and_write_article wiki_output_folder + "/negative/clean_extract_", content
        negative_counter += 1
      end
    end
  end
end

def clean_and_write_article file_prefix, content
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

  File.open(file_prefix + "#{Digest::MD5.hexdigest(content)}", "w") do |f|
    f.write content
  end
end
