arr = []
line_num=0
text=File.open('../data/dewiki-latest-category.sql').read
text.gsub!(/\r\n?/, "\n")
text.each_line do |line|
  line.scan(/'([^']*)',/).each{|w| arr << w}
end

key_words = []
File.open("../data/key_words", "r") do |f|
  f.each_line do |line|
  key_words << line.delete!("\n")
  end
end

File.open("../data/categories", "w+") do |f|
  arr.each do |element| 
    key_words.each do |kword|
      if element.to_s.downcase.gsub(/\s+/, '').include?(kword)
      f.puts(element)
      end
    end
  end
end
