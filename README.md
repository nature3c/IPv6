<h1>Why is my address not unique?</h1>

<h3>Getting the data</h3>
<p>
  IPv6 address were from: https://ipv6observatory.org/ <br>
  The rib files from: https://www.routeviews.org/routeviews/archive/
  CYMRU: https://www.team-cymru.com/ip-asn-mapping
</p>

<h3>Initial data organization</h3>
<p>
  Use the go code (to be put in here) to go through data from the IPv6 Observatory and collect the repeated IPs with high entropy. <br>
  Also, collect the IIDs with high entropy using (to be put in)
</p>

<h3>ASN List</h3>
<p>
  Put the rib file, mrtparse.py, and lookup.py in the same directory. You'll also need to install py-radix.<br>
  ./lookup.py -i &lt;rib&gt; -l &lt;file of ips&gt; <br>
  The output from lookup should be IPv6 address, /32, ASN <br>
  Get the last column of data and remove any duplicated to get unique ASNs and run it through CYMRU's whois. <br>
  You should end up with a text file of ASN Names.
</p>

<h3>Heatmap</h3>
<p>
  Run the IPs through Whois again but use bulk mode so that the output looks like<br>
  ASN | IPv6 Address | Country, CountryCode <br>
  With that list run it through count-asn-country.py and you should get a list of countries counts and ASN counts. <br>
  With those two lists, run it through heatmap.py to get a nice looking heatmap.
</p>

<h3>NTP vs ZMap</h3>
<p>
  
</p>
<h4>Aliased Networks</h4>
<p>
  
</p>

<h3>CDF of IIDs</h3>
<p>
  
</p>

<h3>The issue</h3>
<p>
  
</p>
