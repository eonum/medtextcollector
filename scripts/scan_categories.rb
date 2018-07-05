arr = []
line_num=0
text=File.open(ARGV[0]).read
text.gsub!(/\r\n?/, "\n")
text.each_line do |line|
  line.scan(/'([^']*)',/).each{|w| arr << w}
end

puts("Total number of categories: " + arr.length.to_s)

key_words = ["medizin"]
c = 0

File.open(ARGV[1], "w+") do |f|
  arr.each do |element| 
    key_words.each do |kword|
      if element.to_s.downcase.gsub(/\s+/, '').include?(kword)
	 f.puts(element)
         c += 1
      end
    end
  end
end

puts("Found " + c.to_s + " categories with keywords " + key_words.to_s)
