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
