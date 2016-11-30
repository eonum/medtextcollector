arr = []
line_num=0
text=File.open('../data/dewiki-latest-category.sql').read
text.gsub!(/\r\n?/, "\n")
text.each_line do |line|
	
  arr << line.scan(/'([^']*)'/)
  puts arr
end
arr.compact
File.open("test.txt", "w+") do |f|
  arr.each do |a|
    a.to_s
    if a[].include?('Sport')
      puts a		
      f.puts(a)
    end
  end
end
