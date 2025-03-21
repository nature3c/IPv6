<h1>
  Code I used to look into IPv6 addresses
</h1>
<p>
  Goals: Find why IIDs repeat in IPv6 addresses and fix that<br>
</p>

<h3>So far since September</h3>
<p>
  Made code to take IPv6 addresses with high entropy and sort them by how many times that IID appears<br>
  Proved that this is a problem in at least 3 ISPs, so now find how many more are affected.<br>
  Very fun but processing this much data takes forever. Talking about data, it's from IPv6 Observatory<br>
  Working with Erik Rye is the best.
</p>

<h3>3/10:</h3>
<p>
  I started this GitHub repo <br>
  With the rib file I have the ASNs of the IPv6 addresses so I should find the repeated IIDs and match it to an ASN<br>
  Thoughts - Go through all the unique repeated IIDs and find their /48? With that /48 then find the ASN? 
</p>

<h3>3/11:</h3>
<p>
  Went through with my thoughts from yesterday. I compared my list of unique /48s with the list of the outputs<br>
  from the rib file from the routeviews project. With the list, I removed all the repeats and ran it through<br>
  whois from cymru. Next goal: get counts of IPs by ASN and counts of IPs by country code.
</p>

<h3>3/20</h3>
<p>
  Back from Spring break, finished up the map and country counts. This was my thought process I put in my tasks: <br>
  Take the NTP list and run it through whois from CYMRU. Then, with that list, count how many times each ISP shows up. <br>
  That's part 1: finding the count of  IPs by ASN. Then, part 2: count of IPs by country. Each whois line is formatted <br>
  like "A B DA SILVA MULTIMEDIA - ME, BR," so that the last    part is a country code. Count how many times each country <br>
  code shows up.<br>
  Why did geopandas remove their world map? Anyways heres the map I made. 
  <img src="updated_map.png" alt="map-screenshot">
</p>
