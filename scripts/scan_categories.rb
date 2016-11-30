arr = []
line_num=0
text=File.open('../data/dewiki-latest-category.sql').read
text.gsub!(/\r\n?/, "\n")
text.each_line do |line|
  line.scan(/'([^']*)',/).each{|w| arr << w}
end
File.open("../data/medizin_category.txt", "w+") do |f|
  arr.each do |element| 
    if element.to_s.downcase.gsub(/\s+/, '').include?("medizin")
      f.puts(element)
    end
  end
end
File.open("../data/gesundheit_category.txt", "w+") do |f|
  arr.each do |element|
    if element.to_s.downcase.gsub(/\s+/, '').include?("gesundheit")
      f.puts(element)
    end
  end
end
