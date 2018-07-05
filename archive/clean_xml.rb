require 'nokogiri'

@doc = Nokogiri::XML(File.open("test_top_file_1000.xml"))
@doc.encoding = 'UTF-8'
@doc = @doc.remove_namespaces!

# this variable stores the content of the '<text></text>' tag from the wikipedia xml.
# in the '<text></text>' tag is the usefull content of a wikipedia-site
@wikipedia_text_array = @doc.xpath("//text")

@wikipedia_text_cleaned_array = Array.new

# This Array contains all the expressions which should not appear in the plaintext 
array_clean_expressions = Array.new
array_clean_expressions = ["\n", %q[<text xml:space=\"preserve\"], "<\text>", "'''''", "'''", "''", "{{", "}}", "~~~~", "<s>", "<\s>", "<\s>", "<u>", "<\u>", "<!--", "-->", "======", "=====", "====", "===", "==", "**", "##", "::::", ":::", "::", "&lt;!--", "--&gt;"]

@wikipedia_text_array.each do |i|
  wikipedia_text = i.to_s
  puts wikipedia_text.is_a?(String)

  array_clean_expressions.each do |exp|
    wikipedia_text = wikipedia_text.gsub(exp, " ")
  end

  @wikipedia_text_cleaned_array << wikipedia_text
end
