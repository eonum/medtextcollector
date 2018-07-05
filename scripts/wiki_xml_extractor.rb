require 'rubygems'
require 'nokogiri'

wiki_dump_file = ARGV[0]
wiki_output_folder = ARGV[1]
categories_file = ARGV[2]

# This program dumpxml2wiki reads mediawiki xml files dumped by dumpBackup.php
# on the current directory and transforms them into wiki files which can then
# be modified and uploaded again by pywikipediabot using pagefromfile.py on a mediawiki family site.
# The text of each page is searched with xpath and its title is added on the first line as
# an html comment: this is required by pagefromfile.py.
#
counter = 1
Dir.glob(wiki_dump_file).each do |filename|
  input = Nokogiri::XML(File.new(filename), nil, 'UTF-8')
  puts filename.to_s  # prints the name of each .xml file

  File.open(wiki_output_folder + "/out_dewiki-latest-pages-articles" + "#{counter}" + ".wiki", "w") do |f|
    input.xpath("//xmlns:text").each do |n|
      pptitle = n.parent.parent.at_css "title" # searching for the title
      title = pptitle.content
      f.puts "\n{{-start-}}<!--'''" << title.to_s << "'''-->" << n.content  << "\n{{-stop-}}"
    end
  end
  counter += 1
end


#### this part cleans the extracted text. Script is in progress
# nil in this section are because otherwise it always shows a output in the terminal and this might slow down the script

counter = 1                                                             # reset counter to 1

Dir.glob(wiki_output_folder + "/out_dewiki-latest-pages-articles1*", ).each do |file|
  content = []
  File.open(file, "r:UTF-8") do |f|
    file_content = f.read
    file_content = file_content.gsub(/\n/, ""); nil                       # clean the line breaks
    file_content.scan(/{{-start-}}(.*?){{-stop-}}/).each do |article|     #between each -start- -stop- is one article
      content << article.to_s
    end;
  end;
  puts content.size

  # File.open("test", "w+") do |f|
  #   content.each { |element| f.puts(element) }
  # end; nil

  # get the categories from the categories-files
  categories = []
  File.readlines(categories_file).each do |line|
    line = line.gsub(/\n/, "")
    categories << line
  end; nil

  matched_articles = []


  # extract the articles which match with one category
  content.each do |article|
    catch :categoryfound do
      categories.each do |category|
        if article.include?("[[Kategorie:#{category}]]")
          matched_articles << article
        end
      end
    end
  end; nil

  # clean the matches_articles from wikipedia markups
  matched_articles.map! do |element|
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

  # export the clean articles to a new file
  File.open(wiki_output_folder + "/clean_extract" + "#{counter}", "w") do |f|
    matched_articles.each do |article|
      f.write article
    end
    counter += 1
  end

end; nil
