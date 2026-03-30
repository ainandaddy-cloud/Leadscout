"""
========================================================
  GLOBAL CITIES DATABASE
  Maximum coverage - every district, suburb, neighborhood
========================================================
  Usage in config.py:
    from cities import build_queries, DUBAI
    SEARCH_QUERIES = build_queries(DUBAI, PROFESSION)
========================================================
"""


def build_queries(area_list, profession):
    """Builds search queries dynamically from profession."""
    return [f"{profession} in {area}" for area in area_list]


# ══════════════════════════════════════════════════════
#  INDIA
# ══════════════════════════════════════════════════════

MUMBAI = [
    # Western Suburbs
    "Andheri West Mumbai", "Andheri East Mumbai", "Jogeshwari West Mumbai",
    "Jogeshwari East Mumbai", "Goregaon West Mumbai", "Goregaon East Mumbai",
    "Malad West Mumbai", "Malad East Mumbai", "Kandivali West Mumbai",
    "Kandivali East Mumbai", "Borivali West Mumbai", "Borivali East Mumbai",
    "Dahisar Mumbai", "Mira Road Mumbai", "Bhayander Mumbai",
    "Vasai Mumbai", "Virar Mumbai",
    # Central Suburbs
    "Bandra West Mumbai", "Bandra East Mumbai", "Santacruz West Mumbai",
    "Santacruz East Mumbai", "Vile Parle West Mumbai", "Vile Parle East Mumbai",
    "Juhu Mumbai", "Khar Mumbai", "Linking Road Mumbai",
    # Harbour Line
    "Kurla Mumbai", "Ghatkopar West Mumbai", "Ghatkopar East Mumbai",
    "Vikhroli Mumbai", "Mulund West Mumbai", "Mulund East Mumbai",
    "Bhandup Mumbai", "Nahur Mumbai",
    # South Mumbai
    "Colaba Mumbai", "Nariman Point Mumbai", "Fort Mumbai",
    "Churchgate Mumbai", "Marine Lines Mumbai", "Grant Road Mumbai",
    "Dadar West Mumbai", "Dadar East Mumbai", "Parel Mumbai",
    "Lower Parel Mumbai", "Worli Mumbai", "Prabhadevi Mumbai",
    "Matunga Mumbai", "Sion Mumbai", "Chembur Mumbai",
    "Govandi Mumbai", "Mankhurd Mumbai", "Dharavi Mumbai",
    # Navi Mumbai
    "Vashi Navi Mumbai", "Nerul Navi Mumbai", "Belapur Navi Mumbai",
    "Kharghar Navi Mumbai", "Panvel Mumbai", "Airoli Navi Mumbai",
    "Ghansoli Navi Mumbai", "Kopar Khairane Navi Mumbai",
    # Thane
    "Thane West", "Thane East", "Kalwa Thane", "Mumbra Thane",
    "Dombivli East", "Dombivli West", "Kalyan West", "Kalyan East",
    "Ulhasnagar", "Ambernath", "Badlapur",
]

DELHI = [
    # Central Delhi
    "Connaught Place Delhi", "Karol Bagh Delhi", "Paharganj Delhi",
    "Daryaganj Delhi", "Chandni Chowk Delhi",
    # South Delhi
    "Lajpat Nagar Delhi", "Greater Kailash 1 Delhi", "Greater Kailash 2 Delhi",
    "Malviya Nagar Delhi", "Saket Delhi", "Vasant Kunj Delhi",
    "Vasant Vihar Delhi", "Hauz Khas Delhi", "Green Park Delhi",
    "Safdarjung Delhi", "Defence Colony Delhi", "Jangpura Delhi",
    "Nehru Place Delhi", "Kalkaji Delhi", "Govindpuri Delhi",
    "Okhla Delhi", "Sarita Vihar Delhi", "Badarpur Delhi",
    # West Delhi
    "Dwarka Sector 6 Delhi", "Dwarka Sector 7 Delhi", "Dwarka Sector 10 Delhi",
    "Dwarka Sector 12 Delhi", "Dwarka Sector 14 Delhi", "Dwarka Mor Delhi",
    "Janakpuri Delhi", "Rajouri Garden Delhi", "Uttam Nagar Delhi",
    "Patel Nagar Delhi", "Paschim Vihar Delhi", "Tilak Nagar Delhi",
    "Subhash Nagar Delhi", "Punjabi Bagh Delhi",
    # North Delhi
    "Rohini Sector 3 Delhi", "Rohini Sector 7 Delhi", "Rohini Sector 9 Delhi",
    "Pitampura Delhi", "Shalimar Bagh Delhi", "Ashok Vihar Delhi",
    "Model Town Delhi", "Mukherjee Nagar Delhi", "GTB Nagar Delhi",
    # East Delhi
    "Preet Vihar Delhi", "Shahdara Delhi", "Dilshad Garden Delhi",
    "Mayur Vihar Phase 1 Delhi", "Mayur Vihar Phase 2 Delhi",
    "Patparganj Delhi", "Laxmi Nagar Delhi", "Vivek Vihar Delhi",
    # Noida
    "Noida Sector 18", "Noida Sector 62", "Noida Sector 50",
    "Noida Sector 44", "Noida Sector 137", "Noida Sector 100",
    "Noida Sector 76", "Greater Noida West", "Greater Noida Alpha",
    # Gurgaon
    "Gurgaon Sector 14", "Gurgaon Sector 29", "Gurgaon Sector 56",
    "Gurgaon DLF Phase 1", "Gurgaon DLF Phase 2", "Gurgaon DLF Phase 3",
    "Gurgaon Sohna Road", "Gurgaon Golf Course Road", "Gurgaon MG Road",
    "Gurgaon Palam Vihar", "Gurgaon Udyog Vihar",
    # Faridabad & Ghaziabad
    "Faridabad Sector 15", "Faridabad Sector 21", "Faridabad NIT",
    "Ghaziabad Vaishali", "Ghaziabad Indirapuram", "Ghaziabad Raj Nagar",
    "Ghaziabad Crossings Republik",
]

BANGALORE = [
    # South Bangalore
    "Koramangala 1st Block", "Koramangala 4th Block", "Koramangala 8th Block",
    "HSR Layout Sector 1", "HSR Layout Sector 7", "BTM Layout Bangalore",
    "Jayanagar 4th Block", "JP Nagar Phase 1", "JP Nagar Phase 7",
    "Bannerghatta Road Bangalore", "Begur Road Bangalore",
    "Electronic City Phase 1", "Electronic City Phase 2",
    "Bommanahalli Bangalore", "Hongasandra Bangalore",
    # East Bangalore
    "Indiranagar 1st Stage", "Indiranagar 2nd Stage", "Domlur Bangalore",
    "Whitefield Bangalore", "Marathahalli Bangalore", "Sarjapur Road Bangalore",
    "Bellandur Bangalore", "Kadugodi Bangalore", "Brookefield Bangalore",
    "Varthur Bangalore", "KR Puram Bangalore", "CV Raman Nagar Bangalore",
    "Ulsoor Bangalore", "Halasuru Bangalore",
    # North Bangalore
    "Hebbal Bangalore", "Yelahanka Bangalore", "Kogilu Bangalore",
    "HBR Layout Bangalore", "Hennur Road Bangalore", "Banaswadi Bangalore",
    "RT Nagar Bangalore", "Kalyan Nagar Bangalore",
    # West Bangalore
    "Malleshwaram Bangalore", "Rajajinagar Bangalore", "Vijayanagar Bangalore",
    "Nagarbhavi Bangalore", "Kengeri Bangalore", "Banashankari Bangalore",
    "Basavanagudi Bangalore", "Jayanagar Bangalore",
    # Central Bangalore
    "MG Road Bangalore", "Brigade Road Bangalore", "Richmond Town Bangalore",
    "Lavelle Road Bangalore", "Residency Road Bangalore",
]

HYDERABAD = [
    "Jubilee Hills Hyderabad", "Banjara Hills Road 1", "Banjara Hills Road 12",
    "Hitech City Hyderabad", "Gachibowli Hyderabad", "Madhapur Hyderabad",
    "Kondapur Hyderabad", "Kukatpally Hyderabad", "Begumpet Hyderabad",
    "Secunderabad", "Ameerpet Hyderabad", "SR Nagar Hyderabad",
    "Somajiguda Hyderabad", "Punjagutta Hyderabad", "Dilsukhnagar Hyderabad",
    "LB Nagar Hyderabad", "Uppal Hyderabad", "Nacharam Hyderabad",
    "Miyapur Hyderabad", "Bachupally Hyderabad", "Kompally Hyderabad",
    "Nizampet Hyderabad", "Chandanagar Hyderabad", "Tolichowki Hyderabad",
    "Mehdipatnam Hyderabad", "Attapur Hyderabad", "Nanakramguda Hyderabad",
    "Financial District Hyderabad", "Manikonda Hyderabad", "Nallagandla Hyderabad",
    "Shamshabad Hyderabad", "Peerzadiguda Hyderabad", "Boduppal Hyderabad",
    "Malkajgiri Hyderabad", "Sainikpuri Hyderabad",
]

CHENNAI = [
    "Anna Nagar East Chennai", "Anna Nagar West Chennai",
    "T Nagar Chennai", "Adyar Chennai", "Velachery Chennai",
    "Tambaram Chennai", "Porur Chennai", "Chromepet Chennai",
    "Perambur Chennai", "Ambattur Chennai", "Avadi Chennai",
    "Sholinganallur Chennai", "OMR Perungudi Chennai", "OMR Thoraipakkam Chennai",
    "Nungambakkam Chennai", "Egmore Chennai", "Mylapore Chennai",
    "Thiruvanmiyur Chennai", "Pallavaram Chennai", "Guindy Chennai",
    "Kodambakkam Chennai", "Virugambakkam Chennai", "Mogappair Chennai",
    "Kolathur Chennai", "Madhavaram Chennai", "Tondiarpet Chennai",
    "Royapuram Chennai", "Perungudi Chennai", "Navalur Chennai",
    "Siruseri Chennai", "Medavakkam Chennai", "Pallikaranai Chennai",
    "Nanganallur Chennai", "Alandur Chennai", "Saidapet Chennai",
    "Vadapalani Chennai", "Ashok Nagar Chennai",
]

PUNE = [
    "Koregaon Park Pune", "Kalyani Nagar Pune", "Viman Nagar Pune",
    "Kharadi Pune", "Wakad Pune", "Hinjewadi Phase 1 Pune",
    "Hinjewadi Phase 2 Pune", "Baner Pune", "Balewadi Pune",
    "Aundh Pune", "Kothrud Pune", "Deccan Gymkhana Pune",
    "FC Road Pune", "JM Road Pune", "Shivajinagar Pune",
    "Camp Pune", "Hadapsar Pune", "Fursungi Pune",
    "Kondhwa Pune", "Undri Pune", "Wanowrie Pune",
    "Magarpatta Pune", "Sinhagad Road Pune", "Katraj Pune",
    "Pimpri Pune", "Chinchwad Pune", "Akurdi Pune",
    "Nigdi Pune", "Bhosari Pune", "Wagholi Pune",
    "Sus Road Pune", "Pashan Pune", "Mundhwa Pune",
    "Dhanori Pune", "Lohegaon Pune",
]

AHMEDABAD = [
    "Navrangpura Ahmedabad", "Satellite Ahmedabad", "Vastrapur Ahmedabad",
    "Bodakdev Ahmedabad", "Prahlad Nagar Ahmedabad", "SG Highway Ahmedabad",
    "Maninagar Ahmedabad", "Naroda Ahmedabad", "Chandkheda Ahmedabad",
    "Gota Ahmedabad", "Bopal Ahmedabad", "South Bopal Ahmedabad",
    "Thaltej Ahmedabad", "Vejalpur Ahmedabad", "Nikol Ahmedabad",
    "Vastral Ahmedabad", "Naranpura Ahmedabad", "Paldi Ahmedabad",
    "Ellis Bridge Ahmedabad", "CG Road Ahmedabad", "Gurukul Ahmedabad",
    "Memnagar Ahmedabad", "Ghatlodia Ahmedabad", "Nava Vadaj Ahmedabad",
    "Ranip Ahmedabad", "Shahibaug Ahmedabad", "Sabarmati Ahmedabad",
    "Asarwa Ahmedabad", "Rakhial Ahmedabad", "Odhav Ahmedabad",
]

KOLKATA = [
    "Park Street Kolkata", "Salt Lake Sector 1", "Salt Lake Sector 2",
    "Salt Lake Sector 3", "Salt Lake Sector 5", "New Town Action Area 1",
    "New Town Action Area 2", "Rajarhat Kolkata", "Howrah",
    "Dum Dum Kolkata", "Barasat Kolkata", "Behala Kolkata",
    "Tollygunge Kolkata", "Ballygunge Kolkata", "Alipore Kolkata",
    "Gariahat Kolkata", "Jadavpur Kolkata", "Sonarpur Kolkata",
    "Garia Kolkata", "Kasba Kolkata", "Shyambazar Kolkata",
    "Ultadanga Kolkata", "Belghoria Kolkata", "Serampore Kolkata",
    "Baguiati Kolkata", "Kestopur Kolkata", "Lake Town Kolkata",
    "Dakshineswar Kolkata", "Barrackpore Kolkata", "Madhyamgram Kolkata",
]

JAIPUR = [
    "Malviya Nagar Jaipur", "Vaishali Nagar Jaipur", "Mansarovar Jaipur",
    "Raja Park Jaipur", "Civil Lines Jaipur", "MI Road Jaipur",
    "Tonk Road Jaipur", "Ajmer Road Jaipur", "Sikar Road Jaipur",
    "Jagatpura Jaipur", "Pratap Nagar Jaipur", "Sanganer Jaipur",
    "Murlipura Jaipur", "Nirman Nagar Jaipur", "C Scheme Jaipur",
    "Shyam Nagar Jaipur", "Sodala Jaipur", "Vidhyadhar Nagar Jaipur",
    "Bapu Nagar Jaipur", "Lal Kothi Jaipur", "Durgapura Jaipur",
    "Sitapura Jaipur", "Jhotawara Jaipur",
]

SURAT = [
    "Adajan Surat", "Vesu Surat", "Athwa Surat",
    "Citylight Surat", "Pal Surat", "Althan Surat",
    "Bhatar Surat", "Katargam Surat", "Varachha Surat",
    "Udhna Surat", "Piplod Surat", "Dumas Road Surat",
    "Rander Surat", "Limbayat Surat", "Kapodra Surat",
    "Utran Surat", "Sachin Surat", "Palanpur Surat",
    "Amroli Surat", "Punagam Surat",
]

LUCKNOW = [
    "Hazratganj Lucknow", "Gomti Nagar Lucknow", "Gomti Nagar Extension Lucknow",
    "Aliganj Lucknow", "Indira Nagar Lucknow", "Alambagh Lucknow",
    "Charbagh Lucknow", "Mahanagar Lucknow", "Vikas Nagar Lucknow",
    "Rajajipuram Lucknow", "Jankipuram Lucknow", "Chinhat Lucknow",
    "Faizabad Road Lucknow", "Kanpur Road Lucknow", "Sitapur Road Lucknow",
    "Sushant Golf City Lucknow", "Vrindavan Yojana Lucknow",
    "Shaheed Path Lucknow", "Sultanpur Road Lucknow",
]

NAGPUR = [
    "Dharampeth Nagpur", "Sitabuldi Nagpur", "Sadar Nagpur",
    "Ramdaspeth Nagpur", "Wardha Road Nagpur", "Hingna Nagpur",
    "Katol Road Nagpur", "Kamptee Road Nagpur", "Mankapur Nagpur",
    "Nandanvan Nagpur", "Pratap Nagar Nagpur", "Abhyankar Nagar Nagpur",
    "Laxmi Nagar Nagpur", "Trimurti Nagar Nagpur",
]

BHOPAL = [
    "MP Nagar Zone 1 Bhopal", "MP Nagar Zone 2 Bhopal",
    "Arera Colony Bhopal", "Kolar Road Bhopal", "Shahpura Bhopal",
    "Hoshangabad Road Bhopal", "Ayodhya Nagar Bhopal",
    "Shivaji Nagar Bhopal", "Berasia Road Bhopal",
    "Govindpura Bhopal", "Bittan Market Bhopal",
]

INDORE = [
    "Vijay Nagar Indore", "Scheme 54 Indore", "LIG Colony Indore",
    "AB Road Indore", "Palasia Indore", "Bhanwarkuan Indore",
    "Banganga Indore", "Rau Indore", "Rajwada Indore",
    "Sapna Sangeeta Indore", "Bhawarkuan Indore",
    "Old Palasia Indore", "New Palasia Indore",
]

KOCHI = [
    "Ernakulam South Kochi", "Ernakulam North Kochi", "MG Road Kochi",
    "Edapally Kochi", "Kakkanad Kochi", "Aluva Kochi",
    "Vyttila Kochi", "Palarivattom Kochi", "Kaloor Kochi",
    "Thripunithura Kochi", "Panangad Kochi", "Fort Kochi",
    "Mattancherry Kochi", "Cheranalloor Kochi",
]

COIMBATORE = [
    "RS Puram Coimbatore", "Gandhipuram Coimbatore", "Peelamedu Coimbatore",
    "Saibaba Colony Coimbatore", "Singanallur Coimbatore",
    "Hopes College Coimbatore", "Avinashi Road Coimbatore",
    "Mettupalayam Road Coimbatore", "Podanur Coimbatore",
    "Thudiyalur Coimbatore", "Vadavalli Coimbatore",
]

VISAKHAPATNAM = [
    "MVP Colony Visakhapatnam", "Dwaraka Nagar Visakhapatnam",
    "Seethammadhara Visakhapatnam", "Steel Plant Area Visakhapatnam",
    "Gajuwaka Visakhapatnam", "Madhurawada Visakhapatnam",
    "Rushikonda Visakhapatnam", "Kommadi Visakhapatnam",
]

CHANDIGARH = [
    "Sector 17 Chandigarh", "Sector 22 Chandigarh", "Sector 35 Chandigarh",
    "Sector 43 Chandigarh", "Sector 8 Chandigarh", "Sector 11 Chandigarh",
    "Mohali Phase 7", "Mohali Phase 10", "Mohali Phase 11",
    "Panchkula Sector 10", "Panchkula Sector 20", "Zirakpur Chandigarh",
    "Kharar Chandigarh", "Derabassi Chandigarh",
]

PATNA = [
    "Boring Road Patna", "Bailey Road Patna", "Kankarbagh Patna",
    "Rajendra Nagar Patna", "Ashok Rajpath Patna", "Danapur Patna",
    "Phulwarisharif Patna", "Patliputra Colony Patna",
    "Kidwaipuri Patna", "Gardanibagh Patna",
]

COASTAL_KARNATAKA = [
    "Bhatkal", "Mangalore City Centre", "Mangalore Bejai",
    "Mangalore Hampankatta", "Mangalore Kadri", "Mangalore Kankanady",
    "Udupi", "Manipal", "Kundapur", "Karwar",
    "Sirsi", "Kumta", "Honavar", "Ankola",
    "Bantwal", "Puttur", "Belthangady", "Dharmasthala",
    "Moodabidri", "Sullia",
]

ALL_INDIA = (
    MUMBAI + DELHI + BANGALORE + HYDERABAD + CHENNAI +
    PUNE + AHMEDABAD + KOLKATA + JAIPUR + SURAT +
    LUCKNOW + NAGPUR + BHOPAL + INDORE + KOCHI +
    COIMBATORE + VISAKHAPATNAM + CHANDIGARH + PATNA +
    COASTAL_KARNATAKA
)


# ══════════════════════════════════════════════════════
#  UAE — ALL 7 EMIRATES, EVERY AREA
# ══════════════════════════════════════════════════════

DUBAI = [
    # New Dubai / Marina
    "Dubai Marina", "JBR Dubai", "JLT Cluster A", "JLT Cluster T",
    "JVC Dubai", "JVT Dubai", "Dubai Sports City", "Motor City Dubai",
    "Discovery Gardens Dubai", "Green Community Dubai",
    # Palm & Waterfront
    "Palm Jumeirah", "Dubai Waterfront", "Bluewaters Island Dubai",
    # Downtown & Business
    "Downtown Dubai", "Business Bay Dubai", "DIFC Dubai",
    "Burj Khalifa Area", "City Walk Dubai",
    # Old Dubai
    "Deira Naif", "Deira Rigga", "Deira Al Qusais", "Deira Al Nahda",
    "Bur Dubai Mankhool", "Bur Dubai Satwa", "Karama Dubai",
    "Oud Metha Dubai", "Umm Hurair Dubai",
    # Jumeirah
    "Jumeirah 1", "Jumeirah 2", "Jumeirah 3",
    "Jumeirah Beach Road", "Jumeirah Park", "Jumeirah Islands",
    "Jumeirah Golf Estates",
    # Al Barsha & Surrounds
    "Al Barsha 1", "Al Barsha 2", "Al Barsha 3",
    "Al Barsha South", "Al Quoz Industrial", "Al Quoz Residential",
    # Emirates Hills & Meadows
    "Emirates Hills Dubai", "The Meadows Dubai", "The Springs Dubai",
    "The Lakes Dubai", "Arabian Ranches Dubai", "Mirdif Dubai",
    # New Areas
    "Dubai Hills Estate", "Mohammed Bin Rashid City", "Dubai South",
    "Al Furjan Dubai", "Dubai Silicon Oasis", "International City Dubai",
    "Dragon Mart Dubai", "Academic City Dubai",
    # Muhaisnah & Rashidiya
    "Muhaisnah Dubai", "Al Rashidiya Dubai", "Mirdif Hills Dubai",
    "Dubai Festival City", "Al Warqa Dubai",
]

ABU_DHABI = [
    # Main Island
    "Khalidiyah Abu Dhabi", "Corniche Road Abu Dhabi",
    "Electra Street Abu Dhabi", "Hamdan Street Abu Dhabi",
    "Muroor Road Abu Dhabi", "Airport Road Abu Dhabi",
    "Al Zahiyah Abu Dhabi", "Al Markaziyah Abu Dhabi",
    "Tourist Club Area Abu Dhabi", "Al Bateen Abu Dhabi",
    "Al Mushrif Abu Dhabi", "Al Nahyan Abu Dhabi",
    "Al Manhal Abu Dhabi", "Al Karamah Abu Dhabi",
    "Al Rowdah Abu Dhabi", "Al Manaseer Abu Dhabi",
    # Islands
    "Al Reem Island Abu Dhabi", "Al Maryah Island Abu Dhabi",
    "Yas Island Abu Dhabi", "Saadiyat Island Abu Dhabi",
    "Al Raha Beach Abu Dhabi", "Khalifa City A", "Khalifa City B",
    # Suburbs
    "Mohammed Bin Zayed City", "Shakhbout City Abu Dhabi",
    "Mussafah Industrial", "Mussafah Residential",
    "Baniyas Abu Dhabi", "Madinat Zayed Abu Dhabi",
    # Al Ain
    "Al Ain City Centre", "Al Ain Al Jimi", "Al Ain Al Muwaiji",
    "Al Ain Zakher", "Al Ain Al Markhaniyah", "Al Ain Hili",
]

SHARJAH = [
    "Sharjah City Centre", "Al Nahda Sharjah", "Rolla Square Sharjah",
    "Al Qasimia Sharjah", "Al Majaz 1 Sharjah", "Al Majaz 2 Sharjah",
    "Al Majaz 3 Sharjah", "Al Taawun Sharjah", "Muwaileh Sharjah",
    "Al Khan Sharjah", "Al Yarmook Sharjah", "Abu Shagara Sharjah",
    "Al Gharb Sharjah", "Samnan Sharjah", "Al Qadisiya Sharjah",
    "Al Khalidiya Sharjah", "Industrial Area 1 Sharjah",
    "Industrial Area 12 Sharjah", "Al Jazzat Sharjah",
]

AJMAN = [
    "Ajman City Centre", "Al Rashidiya Ajman", "Al Nuaimia 1 Ajman",
    "Al Nuaimia 2 Ajman", "Al Nuaimia 3 Ajman", "Al Jurf Ajman",
    "Al Hamidiya Ajman", "Al Rumailah Ajman",
    "Emirates City Ajman", "Al Rawda 1 Ajman", "Al Rawda 2 Ajman",
    "Mushairif Ajman", "Al Mowaihat Ajman",
]

RAS_AL_KHAIMAH = [
    "Ras Al Khaimah City", "Al Nakheel RAK", "Al Hamra Village RAK",
    "Mina Al Arab RAK", "Al Dhait RAK", "Khuzam RAK",
    "Al Mairid RAK", "Dafan Al Nakheel RAK", "Al Mamourah RAK",
    "Al Qawasim Corniche RAK",
]

FUJAIRAH = [
    "Fujairah City Centre", "Dibba Al Fujairah", "Khor Fakkan",
    "Kalba Fujairah", "Al Faseel Fujairah", "Al Gurfa Fujairah",
]

UMM_AL_QUWAIN = [
    "Umm Al Quwain City", "Al Raas UAQ", "Al Salama UAQ", "Al Raudah UAQ",
]

ALL_UAE = (
    DUBAI + ABU_DHABI + SHARJAH + AJMAN +
    RAS_AL_KHAIMAH + FUJAIRAH + UMM_AL_QUWAIN
)


# ══════════════════════════════════════════════════════
#  SAUDI ARABIA — COMPLETE
# ══════════════════════════════════════════════════════

RIYADH = [
    "Olaya District Riyadh", "Al Malaz Riyadh", "Al Murabba Riyadh",
    "Al Sulaimaniyah Riyadh", "Al Nakheel Riyadh", "Al Rawdah Riyadh",
    "Al Yasmin Riyadh", "Al Hamra Riyadh", "Al Aqiq Riyadh",
    "Al Wurud Riyadh", "Diplomatic Quarter Riyadh", "King Fahd District Riyadh",
    "Al Ghadir Riyadh", "Al Sahafah Riyadh", "Al Izdihar Riyadh",
    "Hittin Riyadh", "Al Narjis Riyadh", "Al Qirawan Riyadh",
    "Al Maather Riyadh", "Al Batha Riyadh", "Al Malqa Riyadh",
    "Al Wizarat Riyadh", "Al Uraija Riyadh", "Al Naseem Riyadh",
    "Al Rabwah Riyadh", "Al Sulimaniyah Riyadh", "Ash Shuhada Riyadh",
    "Al Wadi Riyadh", "Al Falah Riyadh", "Al Badeah Riyadh",
]

JEDDAH = [
    "Al Balad Jeddah", "Al Andalus Jeddah", "Al Rawdah Jeddah",
    "Al Salamah Jeddah", "Al Naeem Jeddah", "Al Marwah Jeddah",
    "Al Hamra Jeddah", "Al Zahraa Jeddah", "Al Faisaliah Jeddah",
    "Al Shati Jeddah", "Al Khalidiyah Jeddah", "Al Muhammadiyah Jeddah",
    "Obhur Al Shamaliyah Jeddah", "Al Safa Jeddah", "Al Waha Jeddah",
    "Al Azizia Jeddah", "Al Rehab Jeddah", "Al Nuzha Jeddah",
    "Al Bawadi Jeddah", "Al Ajwad Jeddah", "Al Rabwah Jeddah",
    "Al Worood Jeddah", "Al Naseem Jeddah", "Al Basateen Jeddah",
    "Prince Abdulaziz Road Jeddah",
]

MECCA = [
    "Al Aziziah Mecca", "Ajyad Mecca", "Al Masfalah Mecca",
    "Kudai Mecca", "Al Nuzha Mecca", "Batha Quraish Mecca",
    "Jarwal Mecca", "Ash Shara Mecca", "Al Adl Mecca",
    "Al Rusaifah Mecca",
]

MEDINA = [
    "Al Noor Medina", "Al Aziziah Medina", "Quba Medina",
    "Al Haram Medina", "Salam Medina", "Al Iskan Medina",
    "Al Rawabi Medina", "Al Munawarrah Medina",
]

DAMMAM = [
    "Al Khobar Corniche", "Al Khobar Al Thuqbah", "Al Khobar Al Rakah",
    "Dhahran Saudi Arabia", "Qatif Saudi Arabia", "Jubail Saudi Arabia",
    "Al Hamra Dammam", "Al Muraikabat Dammam", "Al Naseem Dammam",
    "Ras Tanura Saudi Arabia", "Abqaiq Saudi Arabia",
]

TAIF = [
    "Taif City Centre", "Al Hawiyah Taif", "Al Shafa Taif",
    "Al Hada Taif", "Al Wasl Taif",
]

ALL_SAUDI = RIYADH + JEDDAH + MECCA + MEDINA + DAMMAM + TAIF


# ══════════════════════════════════════════════════════
#  OTHER GCC
# ══════════════════════════════════════════════════════

KUWAIT = [
    "Sharq Kuwait City", "Qibla Kuwait City", "Dasman Kuwait",
    "Salmiya Block 1 Kuwait", "Salmiya Block 7 Kuwait",
    "Hawalli Kuwait", "Siddiq Kuwait", "Rumaithiya Kuwait",
    "Mishrif Kuwait", "Bayan Kuwait", "Salwa Kuwait",
    "Farwaniya Kuwait", "Ashbeliya Kuwait", "Riqqa Kuwait",
    "Abu Halifa Kuwait", "Mangaf Kuwait", "Fintas Kuwait",
    "Mahboula Kuwait", "Ahmadi Kuwait", "Jahra Kuwait",
    "Bneid Al Qar Kuwait", "Nuzha Kuwait",
]

QATAR = [
    "West Bay Doha", "The Pearl Qatar", "Lusail Marina",
    "Lusail Fox Hills", "Al Sadd Doha", "Al Rayyan Qatar",
    "Madinat Khalifa North Doha", "Madinat Khalifa South Doha",
    "Al Wakrah Qatar", "Al Khor Qatar", "Msheireb Downtown Doha",
    "Al Dafna Doha", "Old Airport Road Doha", "Ain Khaled Qatar",
    "Fereej Bin Omran Doha", "New Salata Doha", "Al Mansoura Qatar",
    "Al Markhiya Qatar", "Muaither Qatar", "Al Gharrafa Qatar",
    "Al Aziziya Qatar", "Al Hilal Qatar",
]

BAHRAIN = [
    "Manama Seef District", "Manama Adliya", "Manama Juffair",
    "Manama Zinj", "Manama Sanabis", "Manama Tubli",
    "Riffa East Bahrain", "Riffa West Bahrain",
    "Hamad Town Bahrain", "Isa Town Bahrain",
    "Budaiya Bahrain", "Muharraq Bahrain", "Sitra Bahrain",
    "Busaiteen Bahrain", "Galali Bahrain", "Amwaj Islands Bahrain",
    "Durrat Al Bahrain",
]

OMAN = [
    "Muscat Qurum", "Muscat Al Khuwair", "Muscat Madinat Sultan Qaboos",
    "Muscat Shatti Al Qurum", "Muscat Seeb", "Muscat Bausher",
    "Muscat Muttrah", "Muscat Ruwi", "Muscat Ghubra",
    "Muscat Al Mouj", "Muscat Azaiba", "Muscat Maabelah",
    "Salalah Oman", "Sohar Oman", "Nizwa Oman",
    "Sur Oman", "Muscat Al Hail",
]

ALL_GCC = ALL_UAE + ALL_SAUDI + KUWAIT + QATAR + BAHRAIN + OMAN


# ══════════════════════════════════════════════════════
#  UNITED KINGDOM
# ══════════════════════════════════════════════════════

LONDON = [
    "Westminster London", "Soho London", "Covent Garden London",
    "Shoreditch London", "Canary Wharf London", "Brixton London",
    "Hackney London", "Islington London", "Camden London",
    "Hammersmith London", "Ealing London", "Croydon London",
    "Stratford London", "Greenwich London", "Lewisham London",
    "Southwark London", "Lambeth London", "Tower Hamlets London",
    "Newham London", "Barking London", "Enfield London",
    "Walthamstow London", "Wimbledon London", "Fulham London",
    "Chelsea London", "Kensington London", "Paddington London",
    "Elephant Castle London", "Peckham London", "Tottenham London",
    "Wood Green London", "Finchley London", "Harrow London",
    "Wembley London", "Uxbridge London", "Romford London",
    "Ilford London", "Clapham London", "Balham London",
    "Tooting London", "Streatham London", "Norwood London",
    "Sutton London", "Kingston London", "Richmond London",
    "Twickenham London", "Hounslow London", "Acton London",
]

MANCHESTER = [
    "Manchester City Centre", "Salford Manchester", "Didsbury Manchester",
    "Withington Manchester", "Chorlton Manchester", "Stretford Manchester",
    "Trafford Manchester", "Stockport Manchester", "Oldham Manchester",
    "Bolton Manchester", "Bury Manchester", "Rochdale Manchester",
    "Ashton under Lyne", "Sale Manchester", "Altrincham Manchester",
    "Wigan Manchester", "Leigh Manchester",
]

BIRMINGHAM = [
    "Birmingham City Centre", "Edgbaston Birmingham", "Solihull Birmingham",
    "Erdington Birmingham", "Selly Oak Birmingham", "Kings Heath Birmingham",
    "Handsworth Birmingham", "Sparkhill Birmingham", "Ladywood Birmingham",
    "Harborne Birmingham", "Moseley Birmingham", "Hall Green Birmingham",
    "Wolverhampton", "West Bromwich", "Sutton Coldfield", "Dudley",
    "Walsall", "Halesowen",
]

LEEDS = [
    "Leeds City Centre", "Headingley Leeds", "Chapel Allerton Leeds",
    "Roundhay Leeds", "Morley Leeds", "Pudsey Leeds",
    "Horsforth Leeds", "Garforth Leeds", "Beeston Leeds",
    "Kirkstall Leeds",
]

GLASGOW = [
    "Glasgow City Centre", "West End Glasgow", "East End Glasgow",
    "Southside Glasgow", "Govan Glasgow", "Partick Glasgow",
    "Shawlands Glasgow", "Rutherglen Glasgow", "Paisley Glasgow",
    "Motherwell Glasgow",
]

EDINBURGH = [
    "Edinburgh Old Town", "Edinburgh New Town", "Leith Edinburgh",
    "Morningside Edinburgh", "Bruntsfield Edinburgh",
    "Newington Edinburgh", "Stockbridge Edinburgh",
    "Portobello Edinburgh", "Corstorphine Edinburgh",
]

LIVERPOOL = [
    "Liverpool City Centre", "Wavertree Liverpool", "Toxteth Liverpool",
    "Aigburth Liverpool", "Woolton Liverpool", "Birkenhead Liverpool",
    "Wallasey Liverpool", "Bootle Liverpool",
]

BRISTOL = [
    "Bristol City Centre", "Clifton Bristol", "Bedminster Bristol",
    "Southville Bristol", "Brislington Bristol", "Horfield Bristol",
    "Filton Bristol",
]

NEWCASTLE = [
    "Newcastle City Centre", "Gateshead Newcastle", "Sunderland",
    "Wallsend Newcastle", "Whitley Bay Newcastle",
]

SHEFFIELD = [
    "Sheffield City Centre", "Ecclesall Road Sheffield",
    "Hillsborough Sheffield", "Rotherham Sheffield",
]

NOTTINGHAM = [
    "Nottingham City Centre", "West Bridgford Nottingham",
    "Arnold Nottingham", "Long Eaton Nottingham",
]

LEICESTER = [
    "Leicester City Centre", "Oadby Leicester",
    "Loughborough Leicester", "Hinckley Leicester",
]

ALL_UK = (
    LONDON + MANCHESTER + BIRMINGHAM + LEEDS + GLASGOW +
    EDINBURGH + LIVERPOOL + BRISTOL + NEWCASTLE +
    SHEFFIELD + NOTTINGHAM + LEICESTER
)


# ══════════════════════════════════════════════════════
#  UNITED STATES
# ══════════════════════════════════════════════════════

NEW_YORK = [
    "Midtown Manhattan New York", "Lower Manhattan New York",
    "Upper East Side New York", "Upper West Side New York",
    "Harlem New York", "Washington Heights New York",
    "Williamsburg Brooklyn", "Park Slope Brooklyn",
    "Bay Ridge Brooklyn", "Flatbush Brooklyn",
    "Crown Heights Brooklyn", "Bushwick Brooklyn",
    "Astoria Queens", "Flushing Queens", "Jamaica Queens",
    "Forest Hills Queens", "Long Island City Queens",
    "Bronx Fordham", "Bronx Riverdale", "Staten Island",
    "Jersey City New Jersey", "Hoboken New Jersey",
    "Newark New Jersey", "Long Island Garden City",
    "White Plains New York", "Yonkers New York",
    "Stamford Connecticut",
]

LOS_ANGELES = [
    "Downtown Los Angeles", "Santa Monica", "Beverly Hills",
    "Hollywood", "West Hollywood", "Koreatown Los Angeles",
    "Silver Lake Los Angeles", "Echo Park Los Angeles",
    "Culver City", "Venice Beach Los Angeles",
    "Pasadena California", "Burbank California",
    "Glendale California", "Torrance California",
    "Inglewood California", "Long Beach California",
    "Anaheim California", "Irvine California",
    "Costa Mesa California", "Santa Ana California",
    "Fullerton California", "Pomona California",
    "Ontario California", "Rancho Cucamonga California",
    "San Bernardino California",
]

CHICAGO = [
    "Downtown Chicago Loop", "Lincoln Park Chicago",
    "Wicker Park Chicago", "Hyde Park Chicago",
    "Pilsen Chicago", "Rogers Park Chicago",
    "Andersonville Chicago", "Evanston Illinois",
    "Oak Park Illinois", "Schaumburg Illinois",
    "Naperville Illinois", "Aurora Illinois",
    "Joliet Illinois", "Waukegan Illinois",
    "Elgin Illinois", "Cicero Illinois",
    "Berwyn Illinois", "Oak Lawn Illinois",
]

HOUSTON = [
    "Downtown Houston", "Midtown Houston", "Galleria Houston",
    "Montrose Houston", "Heights Houston", "Westheimer Houston",
    "Sugar Land Texas", "Katy Texas", "Pearland Texas",
    "The Woodlands Texas", "Pasadena Texas", "Baytown Texas",
    "League City Texas", "Missouri City Texas",
    "Spring Texas", "Humble Texas", "Stafford Texas",
    "Richmond Texas", "Rosenberg Texas",
]

DALLAS = [
    "Downtown Dallas", "Uptown Dallas", "Deep Ellum Dallas",
    "Oak Cliff Dallas", "Plano Texas", "Frisco Texas",
    "McKinney Texas", "Allen Texas", "Arlington Texas",
    "Fort Worth Downtown", "Fort Worth Southside",
    "Irving Texas", "Garland Texas", "Mesquite Texas",
    "Denton Texas", "Carrollton Texas",
    "Richardson Texas", "Lewisville Texas",
    "Flower Mound Texas", "Grapevine Texas",
]

MIAMI = [
    "Downtown Miami", "Miami Beach South Beach",
    "Miami Beach North Beach", "Coral Gables",
    "Brickell Miami", "Wynwood Miami", "Little Havana Miami",
    "Hialeah Florida", "Doral Florida", "Kendall Florida",
    "Aventura Florida", "Pompano Beach Florida",
    "Fort Lauderdale Downtown", "Fort Lauderdale Beach",
    "Hollywood Florida", "Miramar Florida",
    "Pembroke Pines Florida", "Homestead Florida",
]

SAN_FRANCISCO = [
    "Downtown San Francisco", "Mission District San Francisco",
    "Castro San Francisco", "Richmond District San Francisco",
    "Sunset District San Francisco", "SoMa San Francisco",
    "Oakland Downtown", "Oakland Temescal",
    "Berkeley Downtown", "San Jose Downtown",
    "Sunnyvale California", "Santa Clara California",
    "Fremont California", "Hayward California",
    "Palo Alto California", "Mountain View California",
    "Redwood City California", "San Mateo California",
    "Daly City California",
]

PHOENIX = [
    "Downtown Phoenix", "Scottsdale Old Town", "Scottsdale North",
    "Tempe Arizona", "Mesa Arizona", "Chandler Arizona",
    "Gilbert Arizona", "Glendale Arizona",
    "Peoria Arizona", "Surprise Arizona", "Goodyear Arizona",
]

PHILADELPHIA = [
    "Downtown Philadelphia", "South Philadelphia",
    "North Philadelphia", "West Philadelphia",
    "Northeast Philadelphia", "Manayunk Philadelphia",
    "Camden New Jersey", "Cherry Hill New Jersey",
    "Voorhees New Jersey",
]

SEATTLE = [
    "Downtown Seattle", "Capitol Hill Seattle", "Fremont Seattle",
    "Ballard Seattle", "Bellevue Washington",
    "Redmond Washington", "Kirkland Washington",
    "Tacoma Washington", "Renton Washington",
    "Lynnwood Washington", "Everett Washington",
]

BOSTON = [
    "Downtown Boston", "Back Bay Boston", "Fenway Boston",
    "South Boston", "Jamaica Plain Boston",
    "Cambridge Harvard Square", "Cambridge MIT Area",
    "Somerville Massachusetts", "Brookline Massachusetts",
    "Quincy Massachusetts", "Medford Massachusetts",
]

ATLANTA = [
    "Downtown Atlanta", "Midtown Atlanta", "Buckhead Atlanta",
    "Decatur Georgia", "Sandy Springs Georgia",
    "Marietta Georgia", "Smyrna Georgia",
    "Roswell Georgia", "Alpharetta Georgia",
]

LAS_VEGAS = [
    "Las Vegas Strip", "Downtown Las Vegas", "Henderson Nevada",
    "North Las Vegas", "Summerlin Las Vegas",
    "Henderson Green Valley Nevada",
]

DENVER = [
    "Downtown Denver", "Capitol Hill Denver", "Cherry Creek Denver",
    "Aurora Colorado", "Lakewood Colorado",
    "Arvada Colorado", "Westminster Colorado",
    "Englewood Colorado", "Thornton Colorado",
]

SAN_DIEGO = [
    "Downtown San Diego", "Mission Valley San Diego",
    "El Cajon San Diego", "Chula Vista San Diego",
    "Escondido San Diego", "Oceanside San Diego",
    "Carlsbad California", "Encinitas California",
]

SAN_ANTONIO = [
    "Downtown San Antonio", "Alamo Heights San Antonio",
    "Stone Oak San Antonio", "Northside San Antonio",
    "Medical Center San Antonio", "Lackland San Antonio",
]

PORTLAND = [
    "Downtown Portland Oregon", "Pearl District Portland",
    "Southeast Portland", "Northeast Portland",
    "Beaverton Oregon", "Hillsboro Oregon", "Gresham Oregon",
]

ALL_USA = (
    NEW_YORK + LOS_ANGELES + CHICAGO + HOUSTON + DALLAS +
    MIAMI + SAN_FRANCISCO + PHOENIX + PHILADELPHIA +
    SEATTLE + BOSTON + ATLANTA + LAS_VEGAS + DENVER +
    SAN_DIEGO + SAN_ANTONIO + PORTLAND
)


# ══════════════════════════════════════════════════════
#  AUSTRALIA
# ══════════════════════════════════════════════════════

SYDNEY = [
    "Sydney CBD", "Parramatta", "Bondi Junction", "Chatswood",
    "Penrith", "Liverpool NSW", "Blacktown", "Campbelltown NSW",
    "Hornsby", "Hurstville", "Bankstown", "Fairfield NSW",
    "Auburn NSW", "Ryde NSW", "Manly NSW", "Dee Why NSW",
    "Miranda NSW", "Sutherland NSW", "Castle Hill NSW",
    "Baulkham Hills NSW", "Cronulla NSW", "Caringbah NSW",
    "Kogarah NSW", "Burwood NSW", "Strathfield NSW",
]

MELBOURNE = [
    "Melbourne CBD", "St Kilda Melbourne", "Richmond Melbourne",
    "Fitzroy Melbourne", "Brunswick Melbourne", "Footscray Melbourne",
    "Dandenong Melbourne", "Box Hill Melbourne", "Doncaster Melbourne",
    "Ringwood Victoria", "Frankston Melbourne", "Werribee Melbourne",
    "Sunshine Victoria", "Springvale Victoria", "Cranbourne Victoria",
    "Moonee Ponds Melbourne", "Essendon Melbourne", "Coburg Melbourne",
    "Northcote Melbourne", "Preston Melbourne", "Heidelberg Melbourne",
    "Templestowe Melbourne", "Nunawading Melbourne",
    "Croydon Victoria", "Boronia Victoria",
]

BRISBANE = [
    "Brisbane CBD", "South Brisbane", "Fortitude Valley Brisbane",
    "New Farm Brisbane", "West End Brisbane", "Indooroopilly Brisbane",
    "Chermside Brisbane", "Mt Gravatt Brisbane", "Logan Central",
    "Ipswich Queensland", "Toowoomba Queensland",
    "Redland Bay", "Carindale Brisbane", "Wynnum Brisbane",
]

PERTH = [
    "Perth CBD", "Fremantle Perth", "Joondalup Perth",
    "Rockingham Perth", "Mandurah Perth", "Midland Perth",
    "Armadale Perth", "Stirling Perth", "Canning Vale Perth",
    "Cannington Perth", "Morley Perth", "Belmont Perth",
]

ADELAIDE = [
    "Adelaide CBD", "Glenelg Adelaide", "Port Adelaide",
    "Norwood Adelaide", "Marion Adelaide", "Salisbury Adelaide",
    "Mount Barker Adelaide", "Modbury Adelaide",
]

GOLD_COAST = [
    "Surfers Paradise Gold Coast", "Broadbeach Gold Coast",
    "Robina Gold Coast", "Southport Gold Coast",
    "Coolangatta Gold Coast",
]

CANBERRA = [
    "Canberra City", "Belconnen Canberra", "Woden Canberra",
    "Tuggeranong Canberra", "Gungahlin Canberra",
]

ALL_AUSTRALIA = (
    SYDNEY + MELBOURNE + BRISBANE + PERTH +
    ADELAIDE + GOLD_COAST + CANBERRA
)


# ══════════════════════════════════════════════════════
#  NEW ZEALAND
# ══════════════════════════════════════════════════════

NEW_ZEALAND = [
    "Auckland CBD", "Manukau Auckland", "North Shore Auckland",
    "Waitakere Auckland", "Papakura Auckland", "Pukekohe Auckland",
    "Newmarket Auckland", "Takapuna Auckland", "Henderson Auckland",
    "Hamilton New Zealand", "Tauranga New Zealand",
    "Rotorua New Zealand", "Wellington CBD",
    "Lower Hutt Wellington", "Upper Hutt Wellington",
    "Porirua Wellington", "Christchurch CBD",
    "Riccarton Christchurch", "Dunedin New Zealand",
    "Invercargill New Zealand", "Palmerston North New Zealand",
    "Napier New Zealand", "Hastings New Zealand",
    "Nelson New Zealand", "Whangarei New Zealand",
]


# ══════════════════════════════════════════════════════
#  CANADA
# ══════════════════════════════════════════════════════

TORONTO = [
    "Downtown Toronto", "Scarborough Ontario", "Mississauga City Centre",
    "Mississauga Streetsville", "Brampton Ontario",
    "Markham Ontario", "North York Toronto", "Etobicoke Toronto",
    "East York Toronto", "Richmond Hill Ontario",
    "Vaughan Ontario", "Oakville Ontario", "Burlington Ontario",
    "Hamilton Ontario", "Pickering Ontario", "Ajax Ontario",
    "Whitby Ontario", "Oshawa Ontario", "Barrie Ontario",
]

VANCOUVER = [
    "Downtown Vancouver", "Surrey City Centre", "Surrey Newton",
    "Burnaby Metrotown", "Burnaby Brentwood", "Richmond BC",
    "Coquitlam BC", "Langley BC", "Abbotsford BC",
    "North Vancouver BC", "West Vancouver BC",
    "Delta BC", "New Westminster BC", "Port Coquitlam BC",
]

CALGARY = [
    "Downtown Calgary", "Northwest Calgary", "Northeast Calgary",
    "Southeast Calgary", "Southwest Calgary", "Beltline Calgary",
    "Airdrie Alberta", "Cochrane Alberta", "Okotoks Alberta",
]

MONTREAL = [
    "Downtown Montreal", "Plateau Mont Royal Montreal",
    "Rosemont Montreal", "Hochelaga Montreal",
    "Laval Quebec", "Longueuil Quebec",
    "Saint Laurent Montreal", "Lasalle Montreal",
    "Verdun Montreal", "Anjou Montreal",
]

OTTAWA = [
    "Downtown Ottawa", "Gatineau Quebec", "Orleans Ottawa",
    "Kanata Ottawa", "Barrhaven Ottawa", "Nepean Ottawa",
]

EDMONTON = [
    "Downtown Edmonton", "West Edmonton", "South Edmonton",
    "North Edmonton", "St Albert Alberta",
    "Sherwood Park Alberta",
]

WINNIPEG = [
    "Downtown Winnipeg", "St Vital Winnipeg",
    "Transcona Winnipeg", "St James Winnipeg",
    "Polo Park Winnipeg",
]

ALL_CANADA = (
    TORONTO + VANCOUVER + CALGARY + MONTREAL +
    OTTAWA + EDMONTON + WINNIPEG
)


# ══════════════════════════════════════════════════════
#  EUROPE
# ══════════════════════════════════════════════════════

GERMANY = [
    "Berlin Mitte", "Berlin Charlottenburg", "Berlin Kreuzberg",
    "Berlin Prenzlauer Berg", "Berlin Neukolln", "Berlin Schoneberg",
    "Berlin Spandau", "Berlin Marzahn", "Berlin Tempelhof",
    "Munich Maxvorstadt", "Munich Schwabing", "Munich Bogenhausen",
    "Munich Neuhausen", "Munich Pasing", "Munich Sendling",
    "Hamburg City Centre", "Hamburg Altona", "Hamburg Eimsbüttel",
    "Hamburg Harburg", "Hamburg Wandsbek", "Hamburg Barmbek",
    "Frankfurt Sachsenhausen", "Frankfurt Bornheim", "Frankfurt Westend",
    "Frankfurt Nordend", "Frankfurt Bockenheim",
    "Cologne Ehrenfeld", "Cologne Nippes", "Cologne Mulheim",
    "Dusseldorf Altstadt", "Dusseldorf Friedrichstadt",
    "Stuttgart Mitte", "Stuttgart Vaihingen",
    "Leipzig City Centre", "Dresden City Centre",
    "Nuremberg City Centre", "Bremen City Centre",
    "Hanover City Centre", "Dortmund City Centre",
]

SWITZERLAND = [
    "Zurich City 1 Centre", "Zurich City 2 Wollishofen",
    "Zurich City 3 Wiedikon", "Zurich City 4 Aussersihl",
    "Zurich City 6 Unterstrass", "Zurich City 7 Fluntern",
    "Zurich City 8 Riesbach", "Zurich City 10 Höngg",
    "Zurich City 11 Affoltern", "Zurich Oerlikon",
    "Geneva Eaux-Vives", "Geneva Carouge", "Geneva Meyrin",
    "Geneva Lancy", "Geneva Vernier",
    "Basel City Centre", "Basel Kleinbasel", "Basel Allschwil",
    "Bern City Centre", "Bern Bethlehem", "Bern Bümpliz",
    "Lausanne City Centre", "Lausanne Prilly",
    "Winterthur City Centre", "Lucerne City Centre",
    "St Gallen Switzerland",
]

POLAND = [
    "Warsaw Srodmiescie", "Warsaw Mokotow", "Warsaw Ursynow",
    "Warsaw Praga Polnoc", "Warsaw Praga Poludnie", "Warsaw Wola",
    "Warsaw Ochota", "Warsaw Wilanow", "Warsaw Bielany",
    "Krakow Stare Miasto", "Krakow Nowa Huta", "Krakow Podgorze",
    "Krakow Krowodrza", "Krakow Bronowice",
    "Wroclaw Srodmiescie", "Wroclaw Krzyki", "Wroclaw Fabryczna",
    "Poznan City Centre", "Gdansk City Centre", "Gdansk Wrzeszcz",
    "Lodz City Centre", "Katowice City Centre", "Szczecin City Centre",
]

NETHERLANDS = [
    "Amsterdam Centrum", "Amsterdam Oost", "Amsterdam Zuidoost",
    "Amsterdam Noord", "Amsterdam Nieuw-West", "Amsterdam Zuidas",
    "Rotterdam Centrum", "Rotterdam Feijenoord", "Rotterdam Kralingen",
    "Rotterdam Delfshaven",
    "The Hague Centrum", "The Hague Laak", "The Hague Scheveningen",
    "Utrecht Centrum", "Utrecht Overvecht",
    "Eindhoven City Centre", "Tilburg City Centre",
    "Groningen City Centre", "Almere City Centre",
    "Breda City Centre", "Arnhem City Centre",
]

FRANCE = [
    "Paris 1st Louvre", "Paris 3rd Marais", "Paris 4th Ile Saint Louis",
    "Paris 5th Latin Quarter", "Paris 6th Saint Germain",
    "Paris 9th Pigalle", "Paris 10th Republique",
    "Paris 11th Bastille", "Paris 13th Chinatown",
    "Paris 15th Grenelle", "Paris 18th Montmartre",
    "Paris 20th Belleville", "Paris La Defense",
    "Lyon Part Dieu", "Lyon Confluence", "Lyon Croix Rousse",
    "Lyon Presquile", "Lyon Villeurbanne",
    "Marseille Prado", "Marseille Castellane", "Marseille Timone",
    "Toulouse Capitole", "Nice Promenade", "Nice Cimiez",
    "Bordeaux City Centre", "Strasbourg City Centre",
    "Nantes City Centre", "Montpellier City Centre",
    "Rennes City Centre", "Lille City Centre",
]

ITALY = [
    "Rome Prati", "Rome Trastevere", "Rome EUR",
    "Rome Parioli", "Rome Tor Sapienza",
    "Milan Navigli", "Milan Porta Venezia", "Milan Isola",
    "Milan Brera", "Milan Porta Garibaldi", "Milan Moscova",
    "Naples Chiaia", "Naples Vomero", "Naples Fuorigrotta",
    "Turin City Centre", "Turin Crocetta",
    "Florence City Centre", "Florence Oltrarno",
    "Bologna City Centre", "Venice Mestre",
    "Verona City Centre", "Palermo City Centre",
    "Catania City Centre", "Bari City Centre",
]

SPAIN = [
    "Madrid Salamanca", "Madrid Chamberí", "Madrid Retiro",
    "Madrid Tetuan", "Madrid Vallecas", "Madrid Carabanchel",
    "Madrid Pozuelo", "Madrid Alcobendas",
    "Barcelona Eixample Dreta", "Barcelona Eixample Esquerra",
    "Barcelona Gràcia", "Barcelona Sants", "Barcelona Poblenou",
    "Barcelona Sarria", "Barcelona Sant Andreu",
    "Valencia City Centre", "Valencia Ruzafa",
    "Seville City Centre", "Bilbao City Centre",
    "Malaga City Centre", "Malaga Fuengirola",
    "Alicante City Centre", "Murcia City Centre",
    "Zaragoza City Centre", "Palma Mallorca",
]

PORTUGAL = [
    "Lisbon Chiado", "Lisbon Bairro Alto", "Lisbon Alfama",
    "Lisbon Parque das Nações", "Lisbon Belem",
    "Lisbon Cascais", "Lisbon Almada",
    "Porto City Centre", "Porto Matosinhos", "Porto Gaia",
    "Porto Boavista",
    "Braga Portugal", "Faro Portugal", "Algarve Portimao",
    "Algarve Lagos", "Coimbra Portugal",
]

SWEDEN = [
    "Stockholm Norrmalm", "Stockholm Södermalm", "Stockholm Vasastan",
    "Stockholm Östermalm", "Stockholm Kungsholmen",
    "Stockholm Nacka", "Stockholm Solna",
    "Gothenburg City Centre", "Gothenburg Hisingen",
    "Malmö City Centre", "Malmö Hyllie",
    "Uppsala Sweden", "Linköping Sweden",
]

NORWAY = [
    "Oslo City Centre", "Oslo Grünerløkka", "Oslo Frogner",
    "Oslo Majorstuen", "Oslo Bjørvika",
    "Bergen City Centre", "Trondheim City Centre",
    "Stavanger City Centre", "Kristiansand Norway",
]

DENMARK = [
    "Copenhagen Indre By", "Copenhagen Nørrebro", "Copenhagen Vesterbro",
    "Copenhagen Østerbro", "Copenhagen Frederiksberg",
    "Aarhus City Centre", "Odense City Centre",
    "Aalborg Denmark",
]

FINLAND = [
    "Helsinki Kamppi", "Helsinki Kallio", "Helsinki Töölö",
    "Helsinki Pasila", "Espoo Tapiola",
    "Tampere City Centre", "Turku City Centre",
    "Oulu Finland",
]

AUSTRIA = [
    "Vienna Innere Stadt", "Vienna Mariahilf", "Vienna Favoriten",
    "Vienna Floridsdorf", "Vienna Meidling", "Vienna Penzing",
    "Graz City Centre", "Linz City Centre", "Salzburg City Centre",
    "Innsbruck Austria",
]

IRELAND = [
    "Dublin 1 City Centre", "Dublin 2 Southside", "Dublin 4 Ballsbridge",
    "Dublin 6 Rathmines", "Dublin 7 Phibsborough", "Dublin 8 Portobello",
    "Dublin 12 Crumlin", "Dublin 15 Blanchardstown", "Cork City Centre",
    "Galway City Centre", "Limerick City Centre", "Waterford Ireland",
]

CZECH_REPUBLIC = [
    "Prague 1 Old Town", "Prague 2 Vinohrady", "Prague 3 Zizkov",
    "Prague 4 Nusle", "Prague 6 Dejvice", "Prague 7 Holesovice",
    "Brno City Centre", "Ostrava City Centre",
]

BELGIUM = [
    "Brussels City Centre", "Brussels Ixelles", "Brussels Molenbeek",
    "Brussels Schaerbeek", "Brussels Etterbeek",
    "Antwerp City Centre", "Antwerp Borgerhout",
    "Ghent City Centre", "Bruges Belgium", "Liège Belgium",
]

ALL_EUROPE = (
    GERMANY + SWITZERLAND + POLAND + NETHERLANDS + FRANCE +
    ITALY + SPAIN + PORTUGAL + SWEDEN + NORWAY + DENMARK +
    FINLAND + AUSTRIA + IRELAND + CZECH_REPUBLIC + BELGIUM
)


# ══════════════════════════════════════════════════════
#  SOUTHEAST ASIA
# ══════════════════════════════════════════════════════

SINGAPORE = [
    "Orchard Road Singapore", "Marina Bay Singapore", "Bugis Singapore",
    "Tampines Singapore", "Jurong East Singapore", "Woodlands Singapore",
    "Ang Mo Kio Singapore", "Bishan Singapore", "Toa Payoh Singapore",
    "Clementi Singapore", "Bedok Singapore", "Hougang Singapore",
    "Sengkang Singapore", "Yishun Singapore", "Serangoon Singapore",
    "Buona Vista Singapore", "Queenstown Singapore",
]

MALAYSIA = [
    "KLCC Kuala Lumpur", "Bukit Bintang KL", "Chow Kit KL",
    "Bangsar KL", "Mont Kiara KL", "Sri Hartamas KL",
    "Petaling Jaya SS2", "Petaling Jaya Damansara",
    "Subang Jaya SS15", "Shah Alam Seksyen 7",
    "Puchong Malaysia", "Klang Malaysia", "Ampang Malaysia",
    "Johor Bahru City Square", "Johor Bahru Tebrau",
    "Penang Georgetown", "Penang Bayan Lepas", "Penang Butterworth",
    "Ipoh Malaysia", "Kota Kinabalu Malaysia", "Kuching Sarawak",
]

ALL_SEA = SINGAPORE + MALAYSIA


# ══════════════════════════════════════════════════════
#  MASTER — ENTIRE WORLD
# ══════════════════════════════════════════════════════

ALL_WORLD = (
    ALL_INDIA + ALL_GCC + ALL_UK + ALL_USA +
    ALL_AUSTRALIA + NEW_ZEALAND + ALL_CANADA +
    ALL_EUROPE + ALL_SEA
)