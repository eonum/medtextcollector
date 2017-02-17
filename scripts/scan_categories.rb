arr = []
line_num=0
text=File.open('../data/dewiki-latest-category.sql').read
text.gsub!(/\r\n?/, "\n")
text.each_line do |line|
  line.scan(/'([^']*)',/).each{|w| arr << w}
end

key_words = ["Medizin nach Zeit","Mediziner","Alternativmedizin","Medizinische Bildung","Biomedizin","Diagnostik","Medizinische Dokumentation","Epidemiologie","Medizinethik","Ethnomedizin","Evidenzbasierte Medizin","Exkrement","Medizin in Film und Fernsehen","Medizinisches Gebiet","Medizingeschichte","Heilberuf","Medizininformatik","Japanische Medizin","Krankheit","Krankheit als Thema","Medizinische Klassifikation","Naturheilkunde","Organ als Thema","Organisation Medizin","Medizinpreis","Medizinrecht","Sachliteratur Medizin","Sexualmedizin","Medizinstatistik","Strahlenbiologie","Medizintechnik","Therapie","Veterinärmedizi","Medizinische Vorsorg","Zahnmedizin", "medizin", "gesundheit"]

File.open("../data/categories", "w+") do |f|
  arr.each do |element| 
    key_words.each do |kword|
      if element.to_s.downcase.gsub(/\s+/, '').include?(kword)
      f.puts(element)
      end
    end
  end
end
