# Consolidated Findings Register — HP Authentication Suite

**Independent Security Assessment of the HP Authentication Suite**
Prepared by Datasec Solutions Pty Ltd on behalf of Datasec
Version 3.1 · Release date 9 September 2026 · **Client Confidential**

```{=openxml}
<w:tbl><w:tblPr><w:tblStyle w:val="Table"/><w:tblW w:type="dxa" w:w="9412"/><w:tblLayout w:type="fixed"/><w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="0" w:val="0020"/></w:tblPr><w:tblGrid><w:gridCol w:w="3000"/><w:gridCol w:w="6412"/></w:tblGrid><w:tr><w:trPr><w:tblHeader w:val="on"/></w:trPr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="3000"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Document control</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="6412"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve"></w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="3000"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Created</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="6412"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/06/2026</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="3000"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Effective date (current version)</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="6412"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/09/2026</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="3000"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Next review date</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="6412"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">March 2027, or on completion of the deferred live-configuration pass</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
<w:p><w:pPr><w:pStyle w:val="BodyText"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Revision history.</w:t></w:r><w:r><w:t xml:space="preserve"> This document is version-controlled. All changes are recorded below.</w:t></w:r></w:p>
<w:tbl><w:tblPr><w:tblStyle w:val="Table"/><w:tblW w:type="dxa" w:w="9412"/><w:tblLayout w:type="fixed"/><w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="0" w:val="0020"/></w:tblPr><w:tblGrid><w:gridCol w:w="820"/><w:gridCol w:w="1180"/><w:gridCol w:w="2100"/><w:gridCol w:w="5312"/></w:tblGrid><w:tr><w:trPr><w:tblHeader w:val="on"/></w:trPr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Version</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Edit date</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Author</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Summary of amendments</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">1.0</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/06/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Initial release as 03_Findings_Register: 31 findings, 19 components.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">2.0</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">07/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Re-run: 13 components added; delta review of the 19 June-baseline components begun.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">2.1</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">08/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Delta findings filed as counted rows; batch-2 findings and the bearer-scheme sweep verified.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">2.2</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Round-2 consolidation. Every band and score re-derived at source. Estate total settles at 342.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">3.0</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Reissued as two registers on the client’s instruction. Presentation only.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">3.1</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Title page, clickable contents, section page breaks, body aligned to the reference report, every finding restructured on BLUF. No finding, severity, score, vector or count changed.</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
```

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
<w:p><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr><w:r><w:t xml:space="preserve">Contents</w:t></w:r></w:p>
<w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:i/><w:color w:val="595959"/></w:rPr><w:t xml:space="preserve">Every entry below is a link: click it to jump to that section. In Microsoft Word the list can also be refreshed to add page numbers (right-click &gt; Update Field).</w:t></w:r></w:p>
<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \o &quot;1-3&quot; \h \z \u </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X102b2e9de4183984340b81b0bb402a984d3925a"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">1. Executive Summary</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xf2db702bc4c22493d3a3d33224f1ec0cdbd88df"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">1.1 Overall risk ratings, by Target of Evaluation</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xd1091ba33066216bc8daf9ad8825507de3a6f2c"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">1.2 Severity distribution</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xb0f17a21387f6f4865dbb511a68af1aaccd4f9f"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">1.3 Key findings</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xbefff722768bc0d860d1860c698c314016bf8d5"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">1.4 How the counts are constructed, and the qualifiers that travel with them</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xed47a6b243077f0d4d82f02daaee15fbf71e127"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">1.5 Important caveats</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X13de200ec4d4b2cca4efbd9a1c62b80357d14fc"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">2. Overview</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X9500629ddf87d50187daf9dff98960a47019c77"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">2.1 Background</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X2712333080a128c5a6540c042ee4bccda9623a0"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">2.2 Register of findings</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xaad23dfb4afcbd924258802b07bdbd09116c867"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">2.3 In scope</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xf1d43a16ed8bc2972ab6b93af48a5a6a96fbbb9"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">2.4 Testing methodology</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X07df659572f9a3811d1ed70ba5db054b062c00c"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">2.5 Out of scope</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X5440bc35d0f986108c41009ebb902d6fca34470"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">2.6 Report considerations</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X35d4ad8d4024f5cf4e7d8e0f026178dae256ffe"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">2.7 Relationship to the companion register</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X053813bfc1f649a11b9cb58a651dc83468ea4d1"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3. Detailed Findings</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xc51c55a5c4acdb57feb5199f7f98dfd0c81a9ed"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.1 How to read a finding</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xf7bb5282e33ac649b8983a1b6f9a8ff90adbfda"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.2 Critical findings from the newly reviewed components</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X08989556cdb1661311485c34bfd014a75f98434"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.3 Findings that change earlier conclusions</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X99048c39177451866d221ef508d59dab57c1a45"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.4 Delta review, batch 2 — four June-baseline components</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xc89cb30a4056df52cf7b0dd3f162572d953b887"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.5 Bearer-scheme sweep</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X28eeef435a8c5ad4a53190e73eec6c26fe6537e"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.6 Delta review, batch 1 — seven June-baseline components</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X8dcd3ea902d60bc4336cc47fb3facbbcbda8d83"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.7 Delta review, the components reviewed before the session limit</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X2c307d1fd0d7474fed6734d4bc3b7f36da1f13a"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.8 Commercial and product-claim observations</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X6c741546e049586124cdeb053b3dec10bfdd379"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">4. Assurance Observations</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xde86897bfd168b3f689e64037f05a34f134f86c"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">5. Keycloak Retirement Position</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X26d40732965e200c9c0e27bdd5b59ed12cab10d"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">6. Verification Status and Open Items</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X6631b08054fcc8ca5ca302d1031d70fb7ea8856"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">6.1 The per-component verification pass</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xc0c39ce446962328a1c872645b46156238310b4"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">6.2 Round-2 consolidation: what was applied</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X97ddacddd5ead2ab1f2119c8b57f6dfb6a7898b"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">6.3 Open items</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X4037c86bf821d5073dfdc563c946720beaa93ed"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">6.4 What was verified personally at source</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X47ffc6c1c1b08d7c6142570f0d50aed23c62f0f"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">6.5 What is not done</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X8cf020d2cfbf480e417545296e44ec21fed2773"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">7. Appendices</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="appendix-a--testing-methodology"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">Appendix A — Testing methodology</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="appendix-b--vulnerability-ratings"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">Appendix B — Vulnerability ratings</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X4cae5ef2c0beee2d92dae3146981fbdbcced036"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">Appendix C — Reconciliation of the estate total</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="appendix-d--engagement-record"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">Appendix D — Engagement record</w:t></w:r></w:hyperlink></w:p>
<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>
```

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 1. Executive Summary

Datasec commissioned an independent security review of the **HP Authentication Suite** — the HP
Authentication Manager (HPAM) on-device Workpath application, the backend API and token-brokerage
services, the cardless and SignalR QR sign-in flow, the second-party Workpath applications, the
licensing services and PKI, the fleet-deployment tooling, the OXPd card-reader integration, the HPSA
mobile client, and the Microsoft Entra, Graph and Custom Security Attributes integration. The
objective was to establish an evidence-based picture of the suite's security posture before its use
in defence and other regulated customer environments.

The review was conducted as a **static, read-only source-code and configuration assessment** against
industry frameworks — OWASP ASVS, the API Security Top 10, MASVS and the Mobile Top 10, NIST CSF 2.0
and SP 800-53/63, ISO 27001:2022, and GDPR and the Australian Privacy Principles — with each finding
scored under CVSS 3.1. No live, dynamic or penetration testing was performed, and no production or
customer system was contacted. Every finding is cited to source as `file:line`, and where code and
documentation disagreed, the code was treated as authoritative.

**This register records 210 findings against the HP Authentication Suite: 18 Critical, 49 High, 80
Medium, 40 Low and 23 Informational.** The suite has systemic, high-severity weaknesses spanning the
token-trust chain, committed key material, credential and secret handling, transport security, the
licensing trust model and the secure-development lifecycle. On the evidence reviewed, the HP
Authentication Suite in its current source form is **not ready for defence-customer security
assurance** without remediation of the Critical and High findings.

**None of the thirty-one findings raised in June 2026 has been remediated in the three months since.**

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.1 Overall risk ratings, by Target of Evaluation

Based on the discovered vulnerabilities, the following risk ratings are allocated to each area of the
suite.

| Target of Evaluation | Risk rating | Most severe findings |
|---|---|---|
| Backend API and token brokerage (cc-api / hpam-api) | **Critical** | F-01, F-08, F-04, F-17 |
| HP Authentication Manager (HPAM, on-device) | **Critical** | F-02, F-07, F-16, F-03, D-01 |
| Licensing services and PKI | **Critical** | F-11, F-10, F-09, License-Services `NEW-1`, LicenseServer `NEW-1` |
| Infrastructure as code (`infra_hpam`) | **Critical** | `I-D1`, `I-D2`, F-29 |
| Secrets, key and code-signing management (cross-cutting) | **Critical** | F-16, F-12, F-11, F-15 |
| Microsoft Entra / Graph / CSA integration | **Critical** | F-02, F-18 |
| Administration portal and its infrastructure | **Critical** | INFRA-01, INFRA-02, INFRA-03, `ADM-D1` |
| HPSA mobile client (HP Secure Authentication) | **Critical** | CK-01 |
| OXPd card-reader integration | **Critical** | OXPD-01 |
| Document conversion service (pdf-api) | **Critical** | PDF-01 |
| Cardless / SignalR QR sign-in | **High** | F-06, F-05 |
| Second-party Workpath applications | **High** | F-24, F-25, D-OD-01, D-TM-01, D-SP-01 |
| Fleet deployment tooling (HPK, HP-AuthSuite-Manager) | **High** | `H-D1`, `H-D5`, NEW-02 |
| SDLC / CI-CD pipeline and supply chain | **High** | F-21, F-22 |
| Privacy and logging | **High** | F-19, F-06, F-02 |
| Card enrolment tooling | **High** | `D-CC-01`, `D-CC-02` |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.2 Severity distribution

```
Critical       ##########                                      18
High           ############################                    49
Medium         ##############################################  80
Low            #######################                         40
Informational  #############                                   23
               ----------------------------------------------    
TOTAL                                                         210
```

The register is built from six distinct populations of work. They are listed separately because they
were produced by different methods and carry different levels of verification; the distinction
matters when reading any single row.

| Population | Critical | High | Medium | Low | Informational | **Total** |
|---|---|---|---|---|---|---|
| June 2026 baseline register, re-derived at source 2026-09-09 | **8** | **12** | 7 | 2 | — | **29** |
| Components reviewed for the first time in the 2026-09 re-run | **5** | **21** | 25 | 11 | 3 | **65** |
| Delta review, batch 2 — four June-baseline components, verified 2026-09-08 | — | **4** | 2 | 9 | 7 | **22** |
| Bearer-scheme sweep, verified 2026-09-08 | — | — | — | 1 | — | **1** |
| Delta review, batch 1 — seven June-baseline components, re-derived 2026-09-09 | **4** | **8** | 31 | 10 | 9 | **62** |
| Delta review, the components reviewed before the 2026-09-07 session limit | **1** | **4** | 15 | 7 | 4 | **31** |
| **TOTAL — this register** | **18** | **49** | **80** | **40** | **23** | **210** |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.3 Key findings

The dominant themes are summarised below. Full detail, evidence and remediation for each finding
follow in §3.

- **The token-trust chain is broken end to end.** JWT signatures are never cryptographically
 verified anywhere in the suite: the cc-api custom handler accepts any forged or unsigned token
 after only an issuer-string comparison (F-01); the Users API takes the realm from the URL and runs
 every operation under one omnipotent admin account, so any authenticated caller can read or
 reassign any user's Card UID in any tenant (F-08); and the second-party Workpath applications
 consume the handed-off Entra token with no local validation (F-25). The on-device token broker is
 exported and weakly gated, exposing token issuance to a rogue Workpath application (F-07), and
 unflagged broadcast receivers let a co-located application drive sign-in and sign-out with a single
IPC call, bypassing the card reader entirely (`D-01`).
- **Trust-anchor key material is committed to source.** The licensing root CA private key is
 committed in cleartext and embedded in a Generator binary published as a public release asset — a
 full licence-forgery and trust-anchor compromise (F-11). A single Android code-signing key is
 shared and committed across all seven applications with hardcoded keystore passwords (F-12). Live
Entra client secrets and App Configuration master read/write keys are committed to source and to a
 checked-in Terraform state backup (F-16). These are irreversible compromises requiring rotation,
 not merely removal.
- **The licensing decision can be forged without the root key, so rotating it does not fix this.**
The token that tells a device it is licensed is signed by the tenant or device private key, which
 travels inside every licence file, wrapped to a key committed in cleartext. It binds nothing — no
 issuer, audience, expiry or tenant — and the certificate carries no tenant identity. Anyone holding
 any genuine licence file plus the committed API key can mint an accepted `valid:true` for any
 serial and any tenant, indefinitely, without ever touching the root key (License-Services `NEW-1`
 and LicenseServer `NEW-1`, one defect recorded against two products).
- **Plaintext credentials and weak cryptography.** In no-MFA mode the raw OAuth refresh token is
 persisted to Entra Custom Security Attributes as plaintext chunked strings, harvestable by any
 holder of the Graph application token and never cleared on sign-out (F-02). Secrets are written to
 logs and exported to third-party telemetry (F-19). Cryptography across the suite is weak: AES-ECB
 for Card UIDs and customer secrets, hardcoded keys and IVs, a key reused as its own salt, and
 fail-open decryption that accepts tampered or unencrypted data as valid (F-04, F-15, F-23).
- **Transport security is disabled and anonymous surfaces are exposed.** TLS certificate and hostname
 validation is unconditionally disabled on several production HTTP clients (F-03), and in the OXPd
 server the bypass is JVM-global and irreversible, covering the client that carries the Entra client
 secret (OXPD-01). The cardless SignalR hub is anonymous and broadcasts sign-in PII across tenants,
 with a deterministic, replayable printer secret (F-06, F-05). Internet-facing licensing endpoints
 accept unauthenticated upload and validate requests (F-10).
- **The infrastructure as code regenerates the leak it is asked to fix.** `cc-api/main.tf:96` injects
 the App Configuration primary read key as a plaintext application setting into all seven cc-api
 instances, so every `terraform apply` rewrites the Keycloak database password, the bootstrap admin
 password and the ACR password into the state blob. A mutable shared image tag lets any principal
 with registry write access overwrite the exact image all four production Keycloak instances run
 (`I-D1`), and the Terraform identity holds the master credentials the App Services cannot stop
 using (`I-D2`).
- **The secure-development controls that appear to exist do not run.** None of the eighteen CI/CD
 workflows runs SAST, SCA or secret scanning, and a push to `main` auto-deploys to multi-region
 production with no security gate (F-21). The secret-scanning rollout that was credited as the one
 improvement since June is inert: twenty-five workflows pin `actions/checkout@v7`, a major version
 that does not exist, so the job fails before the scanner runs (§3.3).

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.4 How the counts are constructed, and the qualifiers that travel with them

**The estate total across both registers is 28 Critical, 76 High, 126 Medium, 73 Low and 39
Informational, totalling 342.** It balances by row against the seven contributing populations and by
column against the five severity bands. This register holds 210 of those findings and the companion
Datasec register holds 132.

Three qualifiers must travel with the Critical count wherever it is quoted.

1. **Two rows are one defect.** License-Services `NEW-1` and LicenseServer `NEW-1` are the reviewer's
 own declared mirror: one forgeable licensing decision, present in two products. The per-component
 convention counts each component's own findings, so both rows stand, but **18 Critical rows in
 this register are 17 distinct Critical defects**.
2. **Two Criticals turn on one metric, and it has been settled.** `D-01` and June `F-07` were
 re-derived independently by reviewers forbidden to read each other's rows, and both arrived at
Critical 9.2 on the identical vector. The `UI` metric was the whole difference between High and
Critical for both. It was settled at source, for both together, as `UI:N`, and both stand at 9.2.
The evidence is genuinely different in each case, so this is not a double count.
3. **One Critical stands because a proposed downgrade was refused.** A verification seat moved June
`F-02` from Critical to High on the ground that no scoring note recorded a deliberate business
 bucketing. There is one, in the row's own Verification block, and it uses the same construction
 the seat credited elsewhere. The downgrade was refused and the reason is recorded in §6.3.

**One finding is genuinely cross-cutting and is counted once, here, rather than duplicated.** June
`F-21` — the absence of SDLC security gates — records its own affected component as *"All
repositories, CI/CD across the suite"*. It is counted in this register and cross-referenced, without
being counted again, from the companion Datasec register.

**Five rows in the combined estate are printed and not counted, and nothing was deleted.** Three are
marked withdrawals (`D-MF-01`, `DELTA-HP-01`, `DELTA-HP-02`) and two are retained split parents
(`DELTA-MK-03`, `ADM-D3`). A withdrawal is not a deletion: the row keeps its evidence and the
measurement that refuted it, and only its place in the count changes. All five belong to this
register.

**Provenance of the per-component figures.** For the components reviewed for the first time in the
re-run, the per-component figures are as reported by each reviewer. A sample was verified personally
at source, listed in §6.4, not the whole population. Treat any single row as Confirmed only where its
own entry says so.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.5 Important caveats

- **This is a point-in-time assessment.** It is a static review of a provided source snapshot. New
 vulnerabilities and techniques emerge continually, and because exploitation was reasoned rather
 than performed, in order to avoid any production impact, an attacker with greater time and
 resources may surface issues not identified here. The snapshot may also lag the live deployment.
- **Nothing has been re-scored against a live environment.** Every environmental adjustment on the
 reachability-dependent findings still requires the deferred live GitHub, Azure and Entra pass.
Several rows carry explicit revisit gates that a single live datum would fire.
- **Keycloak reachability.** Datasec stated in June 2026 that Keycloak is no longer deployed for
 clients. The code position contradicts that: the infrastructure module is live in all four
 production regions, proven as a five-step chain from the Dockerfile to a deployed App Service, with
 a positive control showing that a disabled module is detectable by the same method. Findings that
 live only on the Keycloak path are retained as valid for the codebase and for legacy and dual-mode
 contexts. See §5.
- **Verification is not uniform across this register, and the differences are stated on each
 section.** The findings from the re-run's deep reviews were each re-derived by an independent
 verifier per component. The batch-2 delta findings had one verifier over twenty-three findings, and
 that pass verified severity bands and their stated bases, not the arithmetic of the scores, because
 no vector string was recorded for those rows. The batch-1 and pre-limit delta findings were
 re-derived at source in round 2 and now carry their vectors. **The two kinds of pass must not be
 summed as one number.**
- **Twenty-three rows still carry no CVSS vector** — the twenty-two batch-2 rows and the one sweep
 row. They were never in a round-2 partition. Their bands are verified; their arithmetic is not.

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 2. Overview

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.1 Background

Datasec engaged an independent reviewer to assess the security of the HP Authentication Suite. The
first assessment was completed on 9 June 2026 and covered nineteen components. A re-run was
commissioned on 7 September 2026, on the client's instruction to *"include the new projects and run
the full test, not just high level"*, which added thirteen components that the first assessment had
never seen and opened a delta review of the nineteen it had.

The re-run's central result is not any single defect. It is that **the June review covered nineteen
of thirty-two components and therefore measured about a fifth of the estate.** The thirteen
components it never saw hold eighty per cent of the third-party dependency surface — 1,780 of 2,198
packages — and produced fifteen Critical findings, none of which existed in the register before the
re-run. Five of those fifteen belong to the HP Authentication Suite and appear in §3.2.

All testing was performed against a provided source snapshot. No live system was contacted.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.2 Register of findings

The findings in this register are presented by the population that produced them. Each population
has its own table in §3, and each row carries its own evidence citation.

| Section | Population | Findings | Verification status |
|---|---|---|---|
| §3.2 | Critical findings from the newly reviewed components | 5 Critical rows, drawn from the 65 findings in those components | Independently re-derived per component |
| §3.3 | Findings that change earlier conclusions | Narrative; the rows they affect are counted in their own sections | Verified as stated on each item |
| §3.4 | Delta review, batch 2 — four June-baseline components | 22 | One independent verifier; bands, not arithmetic |
| §3.5 | Bearer-scheme sweep | 1 | Verified; the aggravator was refuted |
| §3.6 | Delta review, batch 1 — seven June-baseline components | 62 | All re-derived at source in round 2 |
| §3.7 | Delta review, the components reviewed before the session limit | 31 in this register | All re-derived at source in round 2 |
| §3.9 | Commercial and product-claim observations | Not severity-scored | Measured, with controls |
| §1.2 | June 2026 baseline register | 29 in this register | Re-derived at source 2026-09-09 |
| §1.2 | Newly reviewed components, full tally | 65 | Independently re-derived per component |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.3 In scope

Testing covered the following Targets of Evaluation, all as provided source.

- **Backend and token services** — `cc-api` (CypherConnectAPI), `hpam-api`
- **On-device application** — `HPAuthenticationManager` (HPAM)
- **Second-party Workpath applications** — `CypherOneDrive`, `CypherSharePoint`, `Teams`,
`MailFlow`, `UniversalPrint`
- **Shared libraries** — `CommonValueLibraryCypher`, `QuickAccessLibrary`,
`WorkPathApplicationsAndLibrariesSources` (including OnGuardLib)
- **Licensing and PKI** — `License-Services`, `LicenseServer`
- **Administration and marketplace** — `datasec-administration-portal`,
`infra-administration-portal`, `hpam-marketplace`
- **Infrastructure as code** — `infra_hpam`
- **Fleet tooling** — `HPK_Deployment_Utility`, `HP-AuthSuite-Manager`
- **Card and mobile** — `Cyphercard-Enrolment-App`, `CypherKey-cypherkey` (HPSA, HP Secure
Authentication)
- **Card-reader integration** — `OXPd1_solution`
- **Document conversion** — `pdf-api`

**A note on component naming, because it affects how findings must be read.** Component identity in
this engagement is carried by folder name, and two folder names are wrong in a way that inverts
their meaning. The folder named `CypherKey-cypherkey` **is not CypherKey** — it is HPSA, HP Secure
Authentication, the mobile client, identified by `applicationId com.hp.secureauth` and by its own
iOS and Android display names. The product actually called CypherKey lives in the folder named
`OneTimePad` and is a separate Datasec product, carried in the companion register. A finding labelled
"CypherKey" is ambiguous between two authentication products, and the plain-language reading is the
wrong one. Findings in this register use the product identity, not the folder name.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.4 Testing methodology

Please refer to Appendix A for testing-methodology details, and to Appendix B for the severity
rating scheme.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.5 Out of scope

The following were not included.

- Remediation of any vulnerability discovered.
- Denial-of-service and performance testing.
- Live, dynamic or penetration testing of any deployed environment. No production, staging or
 customer system was contacted.
- The live GitHub, Azure and Entra configuration pass, which is deferred and on which several
 reachability questions still depend.
- Decompilation of vendored binary artefacts.
- Anything not specifically listed in §2.3.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.6 Report considerations

This is a point-in-time assessment. New vulnerabilities and attack techniques evolve constantly, and
no service designed to provide protection from security attacks can make network resources
invulnerable to such attacks. Findings are reported structurally: a secret is identified by file,
line and credential class, and **no secret value, prefix or length is reproduced in this document.**

---

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.7 Relationship to the companion register

**Scope of this register, and the predicate used to separate it from its companion.** The client
directed that the findings be issued as two documents: one for the HP Authentication Suite, and one
for the Datasec product projects. A finding is assigned to this register when **its affected
component belongs to the HP Authentication Suite**, judged from that component's own technical
summary and manifest rather than from whether the prose mentions HPAM. Twenty-three of the
thirty-two components under review meet that test. The remaining nine — CryptixWebPortal,
OneTimePad (CypherKey), myPKI, SecurePDF, Reporting Dashboard AU (NexusAI), HPSM, Task-Dispatcher,
Vision Sales Portal and QuickQuote — are carried in `13B_Datasec_Products_Consolidated_Findings_Register_2026-09`.
**Every finding appears in exactly one of the two registers, and the two sum to the estate total of
342.** The one genuinely cross-cutting finding is named in §1.4 rather than duplicated.

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 3. Detailed Findings

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.1 How to read a finding

**Every finding in this section is set out bottom line up front.** A reader who stops after the first
two rows of a finding block knows what is wrong and what to do about it; everything below those two
rows is the supporting detail that lets the conclusion be checked rather than taken on trust.

Each population of findings opens with a **summary table** — identifier, affected component, severity
band, CVSS 3.1 base score and, where a round-2 verifier produced one, the full vector string beside
the score — and is followed by one **finding block** per finding, in the same order. Each block uses
the same six fields, in this order:

| Field | What it carries |
|---|---|
| *(header row)* | The severity band, the CVSS 3.1 base score and vector where one exists, and the affected component. |
| **The issue** | What is wrong, stated as it was filed and verified. This is the bottom line. |
| **Suggested fix** | The single action that addresses it, in one sentence. **Taken from the remediation recorded by the reviewer who raised the finding**, and condensed; where the source review file records no remediation, the row says so and the fix is marked as derived from the defect as measured. |
| **What was tested** | The component and the specific artefacts read, cited to `file:line`, together with the claim that was under test. |
| **How it was tested** | The method — static, read-only source review — the verification pass that applies to that population, and the per-row test record where a verifier wrote one. Where no per-row record exists, the block says so rather than filling the space. |
| **How to resolve** | The full remediation, as recorded by the reviewer who raised the finding, with its source file cited. |

**Where a row deliberately carries no numeric score, it says so and gives the reason** — `n/a, posture
finding`, `n/a, control failure`, `n/a, assurance finding`, `n/a, architectural aggregate, not
additive`, or `n/a, unscoreable from this repository`. That convention was reached independently by
three reviewers and is the round's clearest methodological result: for a control that does not fire,
or a posture baseline that is not met, the fix is not a better number but no number, plus a stated
band and a stated reason. **Where a band was moved during verification, the movement and its basis are
recorded on the finding itself**, so that any reader can re-derive the result rather than take it on
trust.

**Section references inside a finding are those of the superseded register.** Every finding in
this document is reproduced from `13_Consolidated_Findings_Register_2026-09`, the single register
that these two documents replace, and its internal cross-references — `§2.3.3`, `§2.3.5` and the
like — are retained **unchanged**, so that each record still matches its source exactly. The
concordance below maps them onto the sections of the present documents.

| Section in the superseded register | In this register (HPAM) | In the companion register (Datasec) |
|---|---|---|
| §1 Per-component tally | §3.2 | §3.3 |
| §2 The fifteen new Critical findings | §3.2 | §3.2 |
| §2.1 Verification pass | §6.1 | §4.1 |
| §2.2 Findings that change earlier conclusions | §3.3 | — |
| §2.3 Delta review, batch 2 | §3.4 | — |
| §2.3.2 Bearer-scheme sweep | §3.5 | — |
| §2.3.3 Delta review, batch 1 | §3.6 | — |
| §2.3.4 Delta review, the pre-limit components | §3.7 | §3.4 |
| §2.3.5 Coverage-gap review | — | §3.5 |
| §2.3.6 Reconciliation of the estate total | Appendix C | Appendix C |
| §2.3.7 Round-2 consolidation and open items | §6.2 and §6.3 | §4.2 |
| §3 What was verified personally at source | §6.4 | §4.4 |
| §4 Commercial and product-claim observations | §3.8 | §3.6 |
| §5 Assurance observations | §4 | §5 |
| §6 Keycloak retirement position | §5 | §6 |
| §7 What is not done | §6.5 | §4.3 |
| §7.1 Delta-review coverage record | Appendix D | — |


```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.2 Critical findings from the newly reviewed components

Five of the fifteen Critical findings raised by the re-run's first-time reviews belong to the HP
Authentication Suite. **The numbering below is the estate-wide Critical index and is preserved so
that cross-references elsewhere in the assurance pack remain valid; it is not a per-document
sequence.**

**Summary of the Critical findings in this register.** The full record for each — the issue, the suggested fix, and below them what was tested, how it was tested and how to resolve it — follows the table, one finding to a block.

| # | Component | Severity | Finding |
|---|---|---|---|
| 7–8 | infra-administration-portal | **Critical** | Twenty-seven secret-class values committed across dev, staging and production `.tfvar`, including nine Entra client secrets, the portal's database column-encryption key, and five webhook codes that are the sole authenticator on anonymous state-changing production endpoints |
| 9 | HPSA | **Critical** · CVSS 9.3 | A forged provisioning QR takes over the app's identity provider and relay endpoints and exfiltrates a live Entra bearer token |
| 10 | OXPd1 | **Critical** | TLS certificate validation is disabled JVM-globally and irreversibly, covering the client that carries the Entra client secret |
| 12 | pdf-api | **Critical** | The service's only authentication factor is an Entra client secret hardcoded in a shipped Android application |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 7–8 — Twenty-seven secret-class values committed across dev, staging and production `.tfvar`

| Finding **Critical 7–8** | **Critical** · component **infra-administration-portal** |
|---|---|
| **The issue** | **27 secret-class values committed across dev/staging/production `.tfvar`** — nine Entra client secrets, the portal's **EF Core column-encryption key** (consumed at `DataContext.cs:67`), and five webhook codes that are the **sole authenticator** on an `[AllowAnonymous]` `WebhooksController`. Committed production codes make state-changing endpoints (`saas-refresh?reset=true`, `onboarding-cleanup`) effectively public. **dev and staging are byte-identical** (one security domain, two names); production is separate. |
| **Suggested fix** | Treat all twenty-seven values as compromised and rotate every one in every environment, rotating the five production webhook codes first because exploitation of those needs nothing but the value; then remove the `.tfvar` files from version control and move the secrets into Key Vault. |
| **What was tested** | The **infra-administration-portal** Terraform configuration and the ASP.NET portal it provisions, as provided in the source snapshot. The claim under test: that the committed values are secret-class, that they differ per environment, and that the webhook codes are the only authenticator on the endpoints they guard. Artefacts read at the cited lines: `config/*.tfvar` (values reported structurally, never reproduced) · `DataContext.cs:67` · `WebhooksController` · the twelve other controllers used as the control. |
| **How it was tested** | Static, read-only source review of the provided snapshot, followed by an independent verification pass by a reviewer who did not raise the finding. **Verified at source by Wednesday.** The absence of a compensating control was proven three ways rather than asserted: `[AllowAnonymous]` appears exactly once across 498 `.cs` files, the application's global default is authenticated, and all twelve other controllers carry a real policy (§6.1.2). **The inventory itself was corrected upward during verification**: the coordinating reviewer's stated twenty-three keys in `production.tfvar` is in fact thirty-three, with thirty-one each in dev and staging — the instrument had excluded values shorter than fifteen characters, so a floor had been presented as a count (§6.1.3). |
| **How to resolve** | (1) Treat all 27 as compromised and rotate every one in every environment — **including dev and staging, because they are identical to each other** (`INFRA-04`). Rotate the five production webhook codes first: this is the most time-critical rotation in the set, ahead of the Entra secrets, because exploitation needs nothing but the value. (2) Remove `config/*.tfvar` from version control and replace them with a `.tfvars.example` carrying placeholders only; extend `.gitignore` to `*.tfvar`, `*.tfvars`, `*.tfstate`, `*.tfstate.*`. (3) Rewrite repository history with `git filter-repo` or BFG and force-expire GitHub's cached views — but **rotate first and independently**, because history rewriting is not a substitute for rotation. (4) Move the nine per-environment secrets into the Key Vault the application already has. (5) Replace the query-string shared secrets on the webhook endpoints with a real authenticator — Entra-authenticated service-to-service calls, or at minimum an HMAC over body and timestamp with replay rejection, carried in a header rather than in the URL, because query strings are logged by App Service, by Application Insights and by any proxy in front of them. (6) For the column-encryption key, move to a Key Vault reference so the *next* key is never committed, then plan and execute a re-encryption migration per environment, production first. *(Recorded by the reviewer who raised the findings, in `findings-seed-2026-09/infra-administration-portal-main.md`, `INFRA-01` to `INFRA-03`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 9 — A forged provisioning QR takes over the app's identity provider and relay endpoints and exfiltrates a live Entra bearer token

| Finding **Critical 9** | **Critical** · CVSS 3.1 **9.3** · component **HPSA** |
|---|---|
| **The issue** | **A forged provisioning QR takes over the app's IdP and relay endpoints and exfiltrates a live Entra bearer token.** The payload's only integrity protection is AES-GCM under a key hardcoded in the app (`encryptor.dart:8`), so anyone with an APK can mint a valid QR. Delivery: a sticker on a printer console. |
| **Suggested fix** | Stop protecting the QR's integrity with a symmetric key embedded in the client — sign the provisioning payload asymmetrically, with the private key held server-side and a public key pinned in the app — and constrain the endpoints the payload names to an allow-list. |
| **What was tested** | The **HPSA** (HP Secure Authentication) Flutter client, as provided in the source snapshot. The claim under test: that the QR payload's only integrity protection is a symmetric key present in the shipped application, and that the payload can re-point the identity provider and relay endpoints. Artefacts read at the cited lines: `encryptor.dart:8` · the provisioning parser and its consumers · the application identity `com.hp.secureauth`. |
| **How it was tested** | Static, read-only source review of the provided snapshot, followed by an independent verification pass by a reviewer who did not raise the finding. **Verified at source by Wednesday**, including the hardcoded QR key and the application identity. **The band moved during verification and the mechanism did not:** the row was filed Critical 9.3 and re-derived as High 8.2 on the vector alone, because the payload arrives by camera and user action, which CVSS 3.1 §2.1.1 makes `AV:L/UI:R` rather than `AV:N`. **The mechanism is confirmed and is stronger than the finder stated.** The register carries the ruling that its practical deliverability is undiminished — the delivery vector is a sticker on a printer console — and that the bucket change must not drive prioritisation (§6.1.1). |
| **How to resolve** | (1) **Stop protecting QR integrity with a symmetric key embedded in the client.** Sign the provisioning payload asymmetrically: the HPAM console signs with a private key held server-side, and HPSA verifies with a public key pinned in the app. A public key in the binary is harmless; a symmetric key is not. (2) **Allow-list the host.** Constrain `oauthBaseUrl` to the Microsoft identity platform hosts (`login.microsoftonline.com`, `login.microsoftonline.us`, `login.partner.microsoftonline.cn`) and constrain `signalREndpoint` and `baseUrl` to customer-registered domains delivered through a signed, server-controlled channel. (3) Treat every provisioning QR already issued as forgeable and re-provision on the new scheme. *(Recorded by the reviewer who raised the finding, in `findings-seed-2026-09/cypherkey-cypherkey.md`, `CK-01`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 10 — TLS certificate validation is disabled process-wide and irreversibly

| Finding **Critical 10** | **Critical** · component **OXPd1** |
|---|---|
| **The issue** | `NaiveTrustProvider.setAlwaysTrust(true)` at `CombinedServer.java:42`, first statement of `main`. Confirmed from the JAR's constant pool to be **JVM-global and irreversible** (its disable path throws). TLS validation is off for the whole process — including the client carrying the **Entra client secret** and the Graph calls carrying **user access and refresh tokens**. |
| **Suggested fix** | Remove all ten `setAlwaysTrust(true)` calls, and where a self-signed device certificate is genuinely required, build a **scoped** `SSLContext` trusting only a pinned printer certificate and pass it explicitly — never to the default context. |
| **What was tested** | The **OXPd1** LAN server and its client, as provided in the source snapshot, together with the bundled `lib/OXPdLib-1.8.4.jar`. The claim under test: that the trust-provider call is global rather than scoped, and that it is irreversible. Artefacts read at the cited lines: `server/src/CombinedServer.java:41-43,673` · `CardReaderAccessoriesCallbackHandler.java:287` · `PrinterManager.java:44,65,200,254,307` · `RegisterCardReaderSolution.java:72` · `UnregisterCardReaderSolution.java:44` · `MicrosoftAuthService.java:42-44,145-155,431-437,483-489`. |
| **How it was tested** | Static, read-only source review of the provided snapshot, plus read-only inspection of the bundled JAR's constant pool — the archive was extracted to a scratch directory and the class read, not decompiled or executed. The constant pool shows the method installing a provider at position 1, setting `ssl.TrustManagerFactory.algorithm`, and replacing the default hostname verifier, all of which are JVM-wide; and it shows the disable path unimplemented, throwing `UnsupportedOperationException`. **Independently verified at source**; the per-component pass recorded ten confirmations, no refutations and three down-scores for this component (§6.1). |
| **How to resolve** | (1) Remove all ten `setAlwaysTrust(true)` calls. (2) If HP MFPs present self-signed device certificates — the likely motivation — build a **scoped** `SSLContext` trusting only a pinned printer certificate or a private CA, and pass it explicitly to the OXPd proxy factories. **Never to the default context.** (3) Construct the `HttpClient` and the Graph `HttpsURLConnection`s with an explicit `SSLContext` built from the default trust store, so that they cannot inherit a weakened global default even if one is set. (4) Add a startup assertion that fails closed if `ssl.TrustManagerFactory.algorithm` is not the platform default. (5) Rotate the Entra client secret that has been transmitted over unvalidated TLS. *(Recorded by the reviewer who raised the finding, in `findings-seed-2026-09/oxpd1-solution-master.md`, `OXPD-01`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 12 — The service's only authentication factor is an Entra client secret hardcoded in a shipped Android application

| Finding **Critical 12** | **Critical** · component **pdf-api** |
|---|---|
| **The issue** | The service's only auth is App Service Easy Auth, and the credential satisfying it is an **Entra client secret hardcoded in the shipped MailFlow Android app** (`GotenbergCloudRenderingRequestJob.kt:39`). Decompiling the APK yields the whole Gotenberg API. |
| **Suggested fix** | Treat the secret as compromised and rotate it, then remove the client-credentials flow from the mobile client entirely — a public client must not hold a confidential-client secret. |
| **What was tested** | The **pdf-api** Gotenberg service and its Terraform module, together with the MailFlow Android client that authenticates to it, as provided in the source snapshot. The claim under test: that Easy Auth is the only authentication factor, and that the credential satisfying it ships inside a public client. Artefacts read at the cited lines: `GotenbergCloudRenderingRequestJob.kt:39` (the credential reported structurally, never reproduced) · the pdf-api module's `site_config` and Easy Auth configuration · the seven module instantiations. |
| **How it was tested** | Static, read-only source review of the provided snapshot, followed by an independent verification pass by a reviewer who did not raise the finding: nine confirmations, no refutations, one item unverifiable without a live system (§6.1). **One measurement cuts against the finding and is recorded rather than suppressed:** all seven `pdf-api` module instantiations carry `count = 0`, so every control the module declares — Easy Auth, TLS 1.2, HTTPS-only — is switched-off code and any running instance is unmanaged drift (§3.8). **The credential exposure is unaffected by that**, because it is already in released application packages. `PDF-02`, the Gotenberg server-side request forgery, needs the upstream default and could not be settled without network access (§6.1.4). |
| **How to resolve** | (1) Treat the secret as **compromised**; rotate it, and audit the app registration's sign-in logs for use from outside the expected client population. (2) Remove the client-credentials flow from the mobile client entirely — a public client must not hold a confidential-client secret. In order of preference: have MailFlow call the PDF API with the **user's** delegated token, which it already holds, and expose the API with a delegated scope; or put a server-side broker between the client and the API. (3) Resolve the `count = 0` question before anything is attested about this service: either the module is genuinely undeployed, in which case say so, or a running instance exists outside Terraform, in which case its configuration is unknown. **Deleting the dead cloud-rendering class in MailFlow does not discharge this** — the credential is already shipped. *(Recorded by the reviewer who raised the finding, in `findings-seed-2026-09/pdf-api-main.md`, `PDF-01`.)* |

The full per-component tally for the newly reviewed components in this register is as follows.

| Component | Product identity | C | H | M | L | I | Total |
|---|---|---|---|---|---|---|---|
| infra-administration-portal | Terraform IaC, admin portal | **2** | 5 | 2 | 1 | — | 10 |
| HPSA | folder `CypherKey-cypherkey` — HP Secure Authentication | **1** | 4 | 9 | 3 | 1 | 18 |
| OXPd1 solution | HPAM OXPd / card-reader integration | **1** | 7 | 4 | 1 | — | 13 |
| pdf-api | Gotenberg PDF service | **1** | 1 | 5 | 2 | 1 | 10 |
| HP-AuthSuite-Manager | .NET WinUI fleet manager | — | 4 | 5 | 4 | 1 | 14 |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.3 Findings that change earlier conclusions

Six results from the delta reviews change conclusions that earlier reports had published. They are
recorded here because a report that quietly replaces its own earlier statement is harder to audit
than one that shows the correction.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.3.1 The secret-scanning gate is very probably inert, which retracts the one improvement previously credited

| | |
|---|---|
| **The issue** | Twenty-five gitleaks workflows across the estate pin `actions/checkout@v7`, a major version that does not exist, so the job fails at its first step and the scanner never runs. **The one genuine improvement previously credited since June is retracted, and no report may claim that the estate has working secret scanning.** |
| **Suggested fix** | Change the pin to a version that exists, pinned to a commit SHA; read the GitHub Actions run history to confirm the job has never completed; make the job a required status check so a failure blocks a merge; and **re-measure the claim estate-wide before publishing it**, because round 2 found the same pin in at least two further repositories in other partitions. |

**What was tested, how it was tested, and how to resolve it.**

Earlier reporting credited a `gitleaks` CI gate running on push and pull request in twenty-five of
thirty-two components as the single genuine improvement since June. A delta reviewer found, and a
second reader independently verified, that **all twenty-five of those workflows pin
`actions/checkout@v7`, a major version that does not exist.** A workflow whose checkout step cannot
resolve fails before the scanner ever runs.

Measured across every workflow file in the estate:

| `actions/checkout` version pinned | Workflow files | Exists upstream |
|---|---|---|
| `v4` | 35 | yes |
| **`v7`** | **25** | **no — this version does not exist** |
| `v2` | 8 | yes |
| `v3` | 3 | yes |
| `v5` | 1 | yes |
| `v6` | 0 | yes |

All twenty-five `v7` files are gitleaks workflows, and no non-gitleaks workflow uses `v7`. The control
run over the non-gitleaks set returned empty, so the version is exclusive to the security gate:

```
search   actions/checkout@v7   over  .github/workflows/gitleaks.yml   ->  25 files
control  actions/checkout@v7   over  all other workflow files         ->   0 files
```

**Corroborating evidence:** `infra_hpam-main/hpam/terraform.tfstate.backup` still carries the F-16
credentials in a repository whose gitleaks job nominally runs on every push and pull request. A
working gate would have failed that repository months ago.

**Status: suspected, at high confidence.** Settling it requires one look at the GitHub Actions run
history, which a static review cannot reach, and it is the highest-value single item in the deferred
live-configuration pass. **Until then, no report may claim that the estate has working secret
scanning.** The rollout itself still deserves credit: someone added twenty-five workflows, and the
defect is one string.

**This claim is understated and needs re-measuring before it is published.** The inert rollout is
recorded in §3.6 as two rows, `I-D9` and `H-D7`, describing twenty-five repositories. Round 2 found
the identical `@v7` pin in two further repositories in two other partitions — License-Services,
inside `NEW-8`, where the row had filed it as `@v4` and the correction makes the row stronger, and
WorkPathApplications, at `WP-D3`, which is why `WP-D1`'s control is structurally blind. Each reviewer
correctly named it and stopped at the boundary of their own partition, exactly as instructed. The
consequence is structural: four partitions each scoring their own rows cannot produce the finding
that an estate-wide claim is understated by exactly the rows that separate the partitions.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.3.2 Keycloak is wired and load-bearing, not documentation debt

| | |
|---|---|
| **The issue** | The `infra_hpam` Keycloak module is live in all four production regions, proven as a five-step chain from source file to deployed resource. **The code-retirement half of `04_Keycloak_Retirement_Attestation` cannot be attested, and the deployment half is now contradicted rather than merely unevidenced.** This is a live legacy dependency. |
| **Suggested fix** | Withdraw the deployment half of `04_Keycloak_Retirement_Attestation` until the module is genuinely removed from the four production regions, and re-issue the attestation scoped to the three second-party applications that do measure clean against a positive control. |

**What was tested, how it was tested, and how to resolve it.**

The `infra_hpam` Keycloak module is live in all four production regions, proven as a five-step chain
from source file to deployed resource:

```
1  docker/keycloak/Dockerfile          builds the image
2  keycloak-build.yml:39-42            publishes it to the container registry
3  keycloak.V26/main.tf:116-117        consumes that image
4  hpam-service.tf                     instantiates the module 7x, no count guard on any
5  azurerm_linux_web_app               present in Terraform state
```

**Positive control**, which is what makes step 4 a measurement rather than an assumption:

```
control  count = 0  over the 7 pdf-api module instantiations  ->  present on all 7
         so a DISABLED module is detectable by this method; these are not disabled
```

**Consequence for `04_Keycloak_Retirement_Attestation`:** the code-retirement half cannot be
attested, and the deployment half is now contradicted rather than merely unevidenced. This is a live
legacy dependency. The three second-party applications reviewed alongside — MailFlow,
CypherSharePoint and UniversalPrint — measure zero Keycloak references against a positive control on
cc-api, so June's attestation holds for those three.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.3.3 AZU-0047 is retired as a false positive, and the inversion is the real finding

| | |
|---|---|
| **The issue** | The unrestricted-ingress network security group rule that `trivy` flagged Critical is **not deployed**, proven three ways, and should be retired as a false positive on impact. **The real finding is the inversion:** that dead module is the only network-boundary code in the repository, and nothing deployed has a virtual network, private endpoint, security group or web application firewall. |
| **Suggested fix** | Retire `AZU-0047` as a false positive on impact, and carry the absence of any network boundary as the finding it is — it is filed as `I-D10`. **Fix the two latent defects in the dead module before it is ever uncommented:** the unscoped `destination_address_prefix = "*"` and the port-80 cleartext backend rule. |

**What was tested, how it was tested, and how to resolve it.**

The unrestricted-ingress network security group rule flagged Critical by `trivy` **is not deployed**,
proven three ways:

```
1  the security group is never associated with a subnet
2  the module is never instantiated:
       source = "./modules/..."   ->  21 live lines
       the single vnet line       ->  commented out at vnet.tf:6
3  no network resource type has ever been present in Terraform state:
       resource types in state    ->  5 present, 0 of them network types
```

**Retire it as a false positive on impact.**

**The triage inverts into a real finding.** That dead module is the only network-boundary code in the
repository. Nothing deployed has a virtual network, private endpoint, security group or web
application firewall. Two latent defects must be fixed before it is ever uncommented: an unscoped
`destination_address_prefix = "*"`, and a port-80 cleartext backend rule.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.3.4 A tampered manifest reaches the fleet, and the sharp path never touches HP's signature

| | |
|---|---|
| **The issue** | `ValidateHpkFile` is a metadata **extractor** whose name asserts a check it does not perform, and with the plaintext fallback an attacker's manifest is written into the `Hpks` table as a routine upgrade. Arbitrary code execution on the printers is a gap, because HP's device-side signature check is out of scope — **but the config-update and attestation-update paths push manifest-supplied payloads, which by HP's own example carry service URLs, passwords and OAuth client secrets, to already-signed applications with no gate at all.** |
| **Suggested fix** | Delete the plaintext fallback, sign the manifest and the hashes of every bundled `.hpk` and verify before deserialisation, and make `ValidateHpkFile` validate or rename it. **Treat the configuration- and credential-push paths as the sharp edge**, not the APK install path: F-15's `AV:L/PR:L` framing understates them. |

**What was tested, how it was tested, and how to resolve it.**

`ValidateHpkFile` (`HpkServices.cs:27-78`) is a metadata **extractor**, not a validator. It requires
only an `hpk.xml` carrying a `<uuid>`, and any `.apk` yielding a `versionCode`. It never opens
`META-INF` and never checks a signature or a hash. With the plaintext fallback — the attacker simply
does not encrypt — `ImportHpks` writes the attacker's blob into the `Hpks` table, and reusing a known
UUID with a higher `versionCode` reads as a routine upgrade.

Arbitrary code execution on the printers is a **gap**: HP's own guide states that an HPK must be
HP-signed to install, and that check is device-side and out of scope. **But `--config-update --data`
and `--attestation-update --credentials` (`Worker.cs:840` and `:812`) push manifest-supplied payloads
to already-signed applications with no gate at all**, and by HP's own example those payloads carry
service URLs, passwords and OAuth client identifiers and secrets. A tampered manifest can silently
repoint a fleet's configuration and replace its identity credentials. F-15's `AV:L/PR:L` framing
understates this.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.3.5 F-16's remediation cannot be applied as written, and sequence matters

| | |
|---|---|
| **The issue** | **F-16's remediation cannot be applied as written, and the sequence matters.** `cc-api/main.tf:96` injects the App Configuration read key as a plaintext application setting into all seven cc-api instances, so every `terraform apply` rewrites three master credentials into the state blob — Terraform is the mechanism that keeps regenerating the leak. Both App Services' managed identities hold **zero** role assignments, so **revoking the leaked keys today would take the HPAM API down in all seven environments.** The licensing remediations carry two traps of the same kind. |
| **Suggested fix** | Apply in this order and no other: grant the App Services' managed identities `App Configuration Data Reader`; remove the plaintext injection at `cc-api/main.tf:96`; set `local_auth_enabled = false`, which is currently absent and would neutralise every leaked key instantly; **then** rotate. Separately, **fix `TenantLicenseService`'s delete-on-validation-failure behaviour before executing F-11's root rotation**, and treat the committed `LicenseGenerator.exe` and the third undocumented key inside `image_cache.bin` as part of the key inventory, because no text scanner sees either. |

**What was tested, how it was tested, and how to resolve it.**

`cc-api/main.tf:96` injects the App Configuration `primary_read_key` connection string as a plaintext
application setting into all seven cc-api instances, so **every `terraform apply` rewrites the
Keycloak database password, the bootstrap-admin password and the ACR password into the state blob.**
Terraform is the mechanism that keeps regenerating the leak. Both App Services declare
`SystemAssigned` identities holding zero role assignments, and the repository's only role assignment
grants App Configuration Data Owner to whoever last ran `terraform apply` by hand. **Revoking the
leaked keys today would take the HPAM API down in all seven environments.** Setting
`local_auth_enabled = false`, which is currently absent, would neutralise every leaked key instantly,
but only after the identities have been granted a role. **The sequence matters and the register must
carry it.**

The licensing remediations carry two traps of the same kind.

1. **Running F-11's root rotation would destroy the licence table.**
`TenantLicenseService.cs:50-54` **deletes** a tenant's licence row whenever validation fails,
`ValidateLifetime=true` means that expired counts as failed, and the call sits on the default
Tenants page render path. Every stored licence fails against a new root, so the next page view
 wipes them all. **Fix the delete-on-failure behaviour before rotating.**
2. **Deleting the committed `.key` files does not remove the root key from the repository.**
`LicenseGeneratorWin/LicenseGenerator.exe` is committed and contains the root CA private key,
 measured as the same public-key hash as `hpauthsuite_root.key`. No text scanner sees it. The
 committed-key inventory is also larger than the established five: six plain PEM files — the list
 misses `src/License.Portal/Resources/hpam_api_key.pem`, the copy actually loaded at runtime — a
 third undocumented 4096-bit key hidden as gzip inside `image_cache.bin`, twice, and the `.pfx`.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.3.6 F-13's remediation is wrong, though its severity is not

| | |
|---|---|
| **The issue** | **F-13's remediation is wrong, though its severity is not.** The stated fix — add a signature check to `isApplicationPackageGenuine` — would have no effect in three of five applications, because the function is never called there. **A verification that greps `auth.cpp` for a signature check will pass while the gate is fully open.** In UniversalPrint, four of six call sites are additionally commented out. |
| **Suggested fix** | Restore the call sites first, then implement the signature check, and **verify by asserting that `isApplicationAuthorized` returns `false` for an unauthorised caller — not by inspecting the presence of the check.** Consolidate the five private OnGuardLib forks into one versioned artefact so that one fix applies everywhere rather than in two of five applications. |

**What was tested, how it was tested, and how to resolve it.**

The reviewer declined to escalate F-13 and gave the reasoning: the disabled gate protects only
statically extractable constants that F-14 already proves are recoverable offline from the shared
object. **But F-13's stated fix — add a signature check to `isApplicationPackageGenuine` — would have
no effect in three of five applications, because the function is never called.** A verification that
greps `auth.cpp` for a signature check will pass while the gate is fully open. In UniversalPrint,
four of six call sites are additionally commented out.

Also established: **OnGuardLib is five private forks, not one shared library.** Per-file SHA-256
shows genuine divergence in five files; the rest differ only by whitespace and line endings, and the
reviewer said so rather than overclaiming.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.3.7 F-24 no longer reproduces in three of five applications, and that is credited

| | |
|---|---|
| **The issue** | **F-24 no longer reproduces in three of five applications, and that is credited.** The whole attestation module — the hardcoded `dummy_app_token` and the emulator bypasses — is gone from MailFlow, CypherSharePoint and UniversalPrint. This is a genuine removal, and it is the distinction between "removed" and "remediated" applied correctly. |
| **Suggested fix** | No remediation is required for the three applications in which the module is gone. **F-24 remains open for Teams**, which still has it and which is the positive control that makes the removal a measurement rather than a search that found nothing. |

**What was tested, how it was tested, and how to resolve it.**

The whole attestation module — the hardcoded `dummy_app_token` and the emulator bypasses — is **gone**
from MailFlow, CypherSharePoint and UniversalPrint. **Positive control: Teams still has it.** This is
a genuine removal, and it is the distinction between "removed" and "remediated" applied correctly.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.3.8 The licensing decision is forgeable without the root key

| | |
|---|---|
| **The issue** | **The licence file cannot be forged without the root key. The licensing *decision* can.** Both validators are structurally sound and every classic bypass was checked and refuted — but the token that tells a device it is licensed is signed by the tenant key that travels inside every licence file, wrapped to a key committed in cleartext, and it binds nothing: no issuer, audience, expiry or tenant. **Anyone holding any genuine licence file plus the committed API key can mint an accepted `valid:true` for any serial and any tenant, indefinitely, without ever touching the root key — so F-11's root rotation does not fix this.** |
| **Suggested fix** | Stop shipping the signing key inside the artefact it signs for; bind the validation token with `iss`, `aud`, `tenantId`, `exp`, `nbf` and a server-consumed `jti`; and put the tenant identity in the certificate so that chaining to the root stops being the only identity test. Rotate the root key, the API key and the third undocumented 4096-bit key together, and treat every issued licence as compromised. **Add a revocation mechanism**, because today the state is not merely un-revocable but roll-back-able. |

**What was tested, how it was tested, and how to resolve it.**

**The licence file cannot be forged without the root key. The licensing decision can.** Those are
different artefacts, and the distinction is the finding.

Both validators are structurally sound. Every classic bypass was checked and none exists: the trust
anchor is an embedded resource that nothing in the token can influence; there is no
`IssuerSigningKeyResolver` anywhere; `alg:none` fails on `RequireSignedTokens`; HMAC-for-RSA confusion
fails; and all six call sites of `ValidateAsync` were read and all fail closed.

**But the token that tells a device it is licensed is not signed by the root.** It is signed by the
tenant or device private key, which travels inside every licence file, JWE-wrapped to a key committed
in cleartext. And it binds nothing: `LicenseTokenUtils.cs:77-84` and `LicenseServer/Program.cs:292-297`
emit only `{serial, nonce, valid}` — no issuer, audience, expiry, issued-at or tenant — and the
certificate carries no tenant identity either, measured on the committed sample as
`CN=DatasecDevStaging` with no extensions. The documented client check is only that the certificate
chains to the pinned root, which every tenant's certificate passes.

**So anyone holding any genuine licence file plus the committed API key can mint an accepted
`valid:true` for any serial and any tenant, indefinitely, without ever touching the root key.**
F-11's remediation, rotating the root CA, does not fix this. It is a separate Critical, not a variant.

Three further results were established in the same review.

- **One private key wears three hats.** `license_server_api.key` is the TLS server key,
LicenseServer's JWE key, and — measured identical — License.Portal's `hpam_api_key.pem`. That is
 cross-protocol key reuse across two independently deployed products.
- **There is no revocation of any kind.** It is worse than un-revocable: it is roll-back-able,
 because nothing compares an incoming licence to the stored one, so an old, larger licence restores
 quota. The absence is a measurement, not an impression:

```
search   revoc|crl|ocsp|jti|denylist|X509Chain   over both licensing trees  ->   0 hits
control  maxDevices                              over both licensing trees  ->  60 hits
```
- **The gitleaks workflow cannot block a deploy.** It has no `needs:` relationship to the deploy
 workflow, which pushes to `license.hpauthsuite.com` on push to `main`. A gate wired to nothing is
 worse than an absent one, and it partly contradicts F-21's "no SDLC gates" in the same direction as
 the `checkout@v7` finding above.
- **Tenant scoping was enumerated rather than sampled.** `TenantDeviceRepository` is scoped in all
 seven methods. `TenantLicenseRepository` has four unscoped methods; every caller was traced and all
 are gated, so no unscoped query is reachable by a non-home user today, and there is no insecure
 direct object reference on any identifier-bearing handler.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.4 Delta review, batch 2 — four June-baseline components

These twenty-two findings were raised by the overnight delta reviews of four June-baseline
components, the batch that completed the June-baseline delta set at nineteen of nineteen. Full
records, each with explicit found, tested and how fields and a stated statement of what was not
tested, are held in `_Working/delta-review-2026-09/`.

**Verification status.** Every row was re-derived at source on 2026-09-08 by an independent verifier
who did not write it, by opening the cited file and line, confirming the defect is present as
described, and testing the stated basis of its severity. **This pass is deliberately kept separate
from the per-component pass in §6.1, because the two are not the same instrument:** that pass ran one
independent verifier per component, and this one is a single verifier over twenty-three findings.
**No CVSS vector string is recorded for any row below, so what was verified is each row's severity
band and its stated basis, not the arithmetic of its score.**

**Outcome.** Seventeen confirmed as filed; two confirmed with the mechanism restated; two down-scored;
one confirmed with its aggravator refuted; one partly refuted. **None was refuted outright and
nothing moved up** — stated plainly, because a verification pass that only ever confirms is a check
that cannot fail. The four High rows were each pushed on the question that would have moved them, and
each held.

**Summary of the findings in this section.** The full record for each — the issue, the suggested fix, and below them what was tested, how it was tested and how to resolve it — follows the table, one finding to a block.

| ID | Component | Severity | CVSS 3.1 | Finding |
|---|---|---|---|---|
| D-OD-01 | CypherOneDrive | High | 7.1 | The Graph endpoint is inherited from HPAM over IPC and used unvalidated; the bearer token is attached unconditionally to whatever host it names |
| D-OD-02 | CypherOneDrive | Low | 3.3 | `TokenLibraryPermission` is defined by five sibling apps with no `protectionLevel`, is enforced by nothing, and reads in the manifest as a control that does… |
| D-OD-03 | CypherOneDrive | Low | 3.3 | Every user who has ever signed in at the device leaves their email address in an unencrypted preferences key |
| D-OD-04 | CypherOneDrive | Low | 3.1 | The Quick-Access batch sync sends the raw JWT with no `Bearer` scheme, on a client with no DNS fallback and no 401 handling |
| D-OD-05 | CypherOneDrive | Info | n/a | Admin mode is granted on the presence of an intent extra, not its value |
| D-OD-06 | CypherOneDrive | Info | — | Two admin-facing settings are plumbed through the printer's remote-config surface and consumed by nothing |
| D-OD-07 | CypherOneDrive | Info | — | `MIGRATION_NOTES.md` ships a stale, compile-only assurance statement that names three files which no longer exist |
| D-OD-08 | CypherOneDrive | Low | 3.3 | The upload path holds a snapshot of the access token in a `final` field and runs on a third client that cannot refresh it |
| D-TM-01 | Teams | High | 7.1 | Both the Graph endpoint and the OAuth authority are inherited from HPAM over IPC and used unvalidated |
| D-TM-02 | Teams | Medium | 4.3 | Per-user state is keyed on a mutable Entra claim, decoded by a third unverified JWT parser, and collapses to a single shared `"guest"` bucket whenever the… |
| D-TM-03 | Teams | Low | 3.1 | The Quick-Access batch sync sends the raw JWT with no `Bearer` scheme — the identical defect found in CypherOneDrive |
| D-TM-04 | Teams | Low | 3.3 | `disableAccessToken()` does not disable the access token, and sign-out proceeds regardless |
| D-TM-05 | Teams | Info | — | `getGraphServiceClient(token)` accepts a token argument and silently ignores it |
| D-TM-06 | Teams | Info | — | A failed EULA/consent save proceeds into the application anyway |
| D-TM-07 | Teams | Info | — | No CI build or test workflow exists; the only automation on push is a secrets scan |
| D-CVL-01 | CommonValueLibraryCypher | Medium | 5.5 | `isHPCloudUser()` and `isSIOEnabled()` are short-circuited to `false` by a hardcoded `if (true)`, making the suite's only trusted-agent check unreachable |
| D-CVL-02 | CommonValueLibraryCypher | **Low** *(was Medium 5.5)* | — | A fully decrypted copy of a password-protected PDF is written next to the original and never deleted; the temp folder the caller supplies is ignored |
| D-CVL-03 | CommonValueLibraryCypher | **Low** *(was Medium 5.0)* | — | The new shared `WebPageActivity` runs JavaScript in a WebView whose "allowed host" is taken from the very URL it was asked to load, and its abort path loads… |
| D-CVL-04 | CommonValueLibraryCypher | Info | — | The siblings link three different versions of this library, by two different distribution mechanisms |
| D-CC-01 | Cyphercard-Enrolment-App | High | 7.1 | The Android SDK hex-dumps plaintext APDUs — including the enroll-code verification command — to the log in release builds, because the app never turns… |
| D-CC-02 | Cyphercard-Enrolment-App | High | 7.2 | One hardcoded six-digit code authorises fingerprint enrolment and full reset on every card in the estate, and enrolment deliberately leaves the card… |
| D-CC-03 | Cyphercard-Enrolment-App | Low | 2.4 | `android:allowBackup="true"` on an app whose whole purpose is card provisioning |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-OD-01 — The Graph endpoint is inherited from HPAM over IPC and used unvalidated; the bearer token is attached unconditionally to whatever host it names

| Finding `D-OD-01` | **High** · CVSS 3.1 7.1 · component **CypherOneDrive** |
|---|---|
| **The issue** | Graph endpoint inherited from HPAM over IPC, used unvalidated; bearer token attached unconditionally to whatever host it names (consumer half of the HPAM cloud-config defect; three independent consumers incl. a Java file a Kotlin-only sweep would miss) |
| **Suggested fix** | Validate `cloudConfig.graphApi` against a Microsoft national-cloud host allow-list before the Graph client is built, and fail closed; apply the same predicate at the two independent read sites. |
| **What was tested** | The **CypherOneDrive** component, as provided in the source snapshot. The claim under test: *The Graph endpoint is inherited from HPAM over IPC and used unvalidated; the bearer token is attached unconditionally to whatever host it names*. Artefacts read at the cited lines: `common/GraphProvider.kt:50-54,67` · `auth/AuthInterceptor.kt:8-15` · `task/UploadFileTask.java:386` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | In `GraphProvider.init`, before constructing the client, require `cloudConfig.graphApi` to parse as an absolute `https://` URL with no userinfo and no path, and pin its host to the Microsoft national-cloud allow-list (`graph.microsoft.com`, `graph.microsoft.us`, `dod-graph.microsoft.us`, `microsoftgraph.chinacloudapi.cn`). Fail closed — refuse to build the client — rather than falling back. Apply the same predicate at `QuickAccessPresenter.kt:106` and `UploadFileTask.java:386`, or better, remove those two independent reads and route them through one validated accessor. This is worth doing **even after** HPAM is fixed: two independent checks are what stops a single regression from re-opening the path. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cypheronedrive-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-OD-02 — `TokenLibraryPermission` is defined by five sibling apps with no `protectionLevel`, is enforced by nothing, and reads in the manifest as a control that does not exist

| Finding `D-OD-02` | **Low** · CVSS 3.1 3.3 · component **CypherOneDrive** |
|---|---|
| **The issue** | `TokenLibraryPermission` *defined* by five sibling apps with no `protectionLevel` (defaults `normal`), enforced by nothing — a manifest control that does not exist |
| **Suggested fix** | Delete the unenforced `<permission>` element from all five sibling manifests, and declare it once in HPAM at `android:protectionLevel="signature"`. |
| **What was tested** | The **CypherOneDrive** component, as provided in the source snapshot. Artefacts read at the cited lines: five sibling `AndroidManifest.xml` declarations (e.g. `CypherOneDrive-main/app/AndroidManifest.xml:12`) |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Delete the `<permission>` element from all five second-party manifests. If a bespoke permission is wanted, define it **once, in HPAM**, as `android:protectionLevel="signature"`, have the siblings `uses-permission` it, and enforce it with `android:permission=` on `TokenManagementService` and `CloudConfigService` in place of `GET_PACKAGE_SIZE`. Leaving a permission declared but unenforced is worse than not declaring it. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cypheronedrive-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-OD-03 — Every user who has ever signed in at the device leaves their email address in an unencrypted preferences key

| Finding `D-OD-03` | **Low** · CVSS 3.1 3.3 · component **CypherOneDrive** |
|---|---|
| **The issue** | Every user who ever signed in leaves their email address in a plaintext `SharedPreferences` key on the shared MFP; keys never removed |
| **Suggested fix** | Move `EULA_PREFS` into the `EncryptedSharedPreferences` the app already initialises, and key it on the opaque `oid` rather than the user's email address. |
| **What was tested** | The **CypherOneDrive** component, as provided in the source snapshot. The claim under test: *Every user who has ever signed in at the device leaves their email address in an unencrypted preferences key*. Artefacts read at the cited lines: `storage/UserPreferencesStore.kt:156-157` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Move `EULA_PREFS` to `EncryptedSharedPreferences` (the app already initialises one at `SecuredPreferences.kt:15-25`), and key it on the token's `oid` — an opaque GUID — rather than `unique_name`. Prune entries for users who have not signed in within a retention window, and clear on device reset. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cypheronedrive-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-OD-04 — The Quick-Access batch sync sends the raw JWT with no `Bearer` scheme, on a client with no DNS fallback and no 401 handling

| Finding `D-OD-04` | **Low** · CVSS 3.1 3.1 · component **CypherOneDrive** |
|---|---|
| **The issue** | Quick-Access batch sync sends the raw JWT with no `Bearer` scheme, on a client with no DNS fallback and no 401 handling |
| **Suggested fix** | Send the token through the configured Graph client, or at minimum prefix `Bearer `, and surface the HTTP status code on failure. |
| **What was tested** | The **CypherOneDrive** component, as provided in the source snapshot. Artefacts read at the cited lines: `ui/main/presenter/QuickAccessPresenter.kt:114-119` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Route this call through `GraphProvider.getGraphServiceClient()`'s OkHttp client, or at minimum prefix `"Bearer "` and reuse the configured client. Replace `emitter.onError(Throwable())` with an error carrying `response.code` so a 401 is visible. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cypheronedrive-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-OD-05 — Admin mode is granted on the presence of an intent extra, not its value

| Finding `D-OD-05` | **Info** · CVSS 3.1 n/a · component **CypherOneDrive** |
|---|---|
| **The issue** | Admin mode granted on the *presence* of an intent extra, not its value (not externally reachable today) |
| **Suggested fix** | Read the extra's value rather than its presence: `getIntent().getBooleanExtra(EXTRA_LOCAL_ADMIN, false)`. |
| **What was tested** | The **CypherOneDrive** component, as provided in the source snapshot. Artefacts read at the cited lines: `SettingsAppActivity` (`hasExtra(EXTRA_LOCAL_ADMIN)`) |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | `getIntent().getBooleanExtra(EXTRA_LOCAL_ADMIN, false)`. One-line change; removes the class. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cypheronedrive-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-OD-06 — Two admin-facing settings are plumbed through the printer's remote-config surface and consumed by nothing

| Finding `D-OD-06` | **Info** · no CVSS score recorded · component **CypherOneDrive** |
|---|---|
| **The issue** | Two admin-facing settings (`DOMAIN_HINT`, `URL_ADDRESS_BAR`) round-trip the printer's remote-config surface and are read **only by the settings screens that set them** — neither reaches an auth request or any other functional path, and the domain-hint menu's only call site is commented out. |
| **Suggested fix** | Decide the two settings' fate — wire them to the sign-in path, or delete the config keys and their settings screens — and validate `domainHint` as a domain. |
| **What was tested** | The **CypherOneDrive** component, as provided in the source snapshot. The claim under test: *Two admin-facing settings are plumbed through the printer's remote-config surface and consumed by nothing*. Artefacts read at the cited lines: `utils/AppConfigHelper.java:65-171` · `ui/settings/SettingsAppFragment.java:122` (commented-out call site), `:177,308` · `ui/settings/urlbar/SettingsSignInUrlBarFragment.kt:89` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed, wording restated** (§3.4.1). **Test record.** *[wording corrected at verification 2026-09-08: the original "consumed by no code path" was too strong — they are consumed, by their own UI]* |
| **How to resolve** | Decide: wire them to the sign-in path, or delete the config keys, the two settings packages and their `AppConfigHelper` branches. If they are kept, enable minification so dead UI does not ship, and validate `domainHint` as a domain (it is currently a free-text `EditText`, `ui/settings/domainhint/SettingsDomainHintOptionFragment.kt:29`, `etDomainHint.text.toString().trim()`). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cypheronedrive-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-OD-07 — `MIGRATION_NOTES.md` ships a stale, compile-only assurance statement that names three files which no longer exist

| Finding `D-OD-07` | **Info** · no CVSS score recorded · component **CypherOneDrive** |
|---|---|
| **The issue** | `MIGRATION_NOTES.md` ships a stale compile-only assurance statement naming three files that no longer exist — `[CONFLICT]`, code authoritative |
| **Suggested fix** | Regenerate or delete `MIGRATION_NOTES.md`; a stale assurance statement is worse than none. |
| **What was tested** | The **CypherOneDrive** component, as provided in the source snapshot. Artefacts read at the cited lines: `MIGRATION_NOTES.md` vs tree |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Regenerate or delete. If kept, add the release-variant compile and Java compilation to the evidence, and reconcile the file list. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cypheronedrive-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-OD-08 — The upload path holds a snapshot of the access token in a `final` field and runs on a third client that cannot refresh it

| Finding `D-OD-08` | **Low** · CVSS 3.1 3.3 · component **CypherOneDrive** |
|---|---|
| **The issue** | Upload path snapshots the access token into a `final` field at construction, on a third client that cannot refresh — mid-upload refresh never reaches it, 401 never retried |
| **Suggested fix** | Read the access token at call time rather than snapshotting it at construction, and build the upload clients from the shared `GraphProvider` client. |
| **What was tested** | The **CypherOneDrive** component, as provided in the source snapshot. The claim under test: *The upload path holds a snapshot of the access token in a `final` field and runs on a third client that cannot refresh it*. Artefacts read at the cited lines: `task/UploadFileTask.java:85,440` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Read the token at call time rather than at construction (`SecuredPreferences.getAccessToken()` inside `createUploadSession`), and build these three clients from the shared `GraphProvider` client so that DNS fallback, auth and refresh are inherited rather than reimplemented. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cypheronedrive-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-TM-01 — Both the Graph endpoint and the OAuth authority are inherited from HPAM over IPC and used unvalidated

| Finding `D-TM-01` | **High** · CVSS 3.1 7.1 · component **Teams** |
|---|---|
| **The issue** | Graph endpoint **and** OAuth authority inherited from HPAM over IPC, used unvalidated — incl. the sign-out URL; scope `Files.ReadWrite.All ChannelMessage.Send` raises the harvested-token blast radius |
| **Suggested fix** | Validate `graphApi` and `oAuthAuthority` against the national-cloud allow-list in `AppAuthManager.init` and fail closed. |
| **What was tested** | The **Teams** component, as provided in the source snapshot. The claim under test: *Both the Graph endpoint and the OAuth authority are inherited from HPAM over IPC and used unvalidated*. Artefacts read at the cited lines: `auth/AppAuthManager.kt:113` · `auth/AppAuthConstants.kt:16` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | In `AppAuthManager.init`, require `graphApi` and `oAuthAuthority` to parse as absolute `https://` URLs with no userinfo and no path, and pin each host to the Microsoft national-cloud allow-list. Fail closed. Apply the same predicate at `QuickAccessPresenter.kt:89` and `AppAuthManager.kt:113`, or route both through one validated accessor. Do this **even after** HPAM is fixed — two checks are what stops one regression re-opening the path. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/teams-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-TM-02 — Per-user state is keyed on a mutable Entra claim, decoded by a third unverified JWT parser, and collapses to a single shared `"guest"` bucket whenever the parse fails

| Finding `D-TM-02` | **Medium** · CVSS 3.1 4.3 · component **Teams** |
|---|---|
| **The issue** | Per-user state keyed on mutable `preferred_username` first / stable `oid` last, decoded by a third unverified hand-rolled JWT parser; every failed parse collapses to one shared `"guest"` bucket — consent-record integrity; the component's only identity primitive |
| **Suggested fix** | Key per-user state on `tid/oid`, keep `preferred_username` for display only, and stop collapsing failed parses into a shared `"guest"` bucket. |
| **What was tested** | The **Teams** component, as provided in the source snapshot. The claim under test: *Per-user state is keyed on a mutable Entra claim, decoded by a third unverified JWT parser, and collapses to a single shared `"guest"` bucket whenever the parse fails*. Artefacts read at the cited lines: `storage/UserPreferencesStore.kt:130-141,184-196` · `ui/splash/SplashActivity.kt:292-294` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Reorder to `oid` first (ideally `"$tid/$oid"`, which is globally unique and non-reassignable), and keep `preferred_username`/`upn` for **display only** — `currentUserEmail()` is the right place for those. Replace `?: "guest"` with a nullable return (`String?`) so callers must decide what an unidentifiable session means; at minimum, treat it as "not yet accepted" rather than "same as last time". Move `EULA_PREFS` to the `EncryptedSharedPreferences` the app already initialises. Consolidate the three JWT parsers in this suite into one that verifies before it reads. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/teams-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-TM-03 — The Quick-Access batch sync sends the raw JWT with no `Bearer` scheme — the identical defect found in CypherOneDrive

| Finding `D-TM-03` | **Low** · CVSS 3.1 3.1 · component **Teams** |
|---|---|
| **The issue** | Quick-Access batch sync sends the raw JWT with no `Bearer` scheme — identical defect to D-OD-04 (shared-code shape) |
| **Suggested fix** | Prefix `Bearer ` at `QuickAccessPresenter.kt:102`, or route the call through `AppAuthManager.getGraphServiceClient()`. |
| **What was tested** | The **Teams** component, as provided in the source snapshot. Artefacts read at the cited lines: `ui/main/presenter/QuickAccessPresenter.kt:98-103` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Prefix `"Bearer "` at `:102`, or route the call through `AppAuthManager.getGraphServiceClient()`. Report `response.code` on failure. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/teams-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-TM-04 — `disableAccessToken()` does not disable the access token, and sign-out proceeds regardless

| Finding `D-TM-04` | **Low** · CVSS 3.1 3.3 · component **Teams** |
|---|---|
| **The issue** | `disableAccessToken()` does not disable the access token (unauthenticated GET to the logout endpoint, no token sent); local copy cleared, token valid at Microsoft until natural expiry |
| **Suggested fix** | Either rename `disableAccessToken()` to what it actually does, or make it revoke the refresh token through Graph and treat a failure to revoke as a reportable event. |
| **What was tested** | The **Teams** component, as provided in the source snapshot. The claim under test: *`disableAccessToken()` does not disable the access token, and sign-out proceeds regardless*. Artefacts read at the cited lines: `auth/AppAuthManager.kt:101-128` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Rename to reflect what it does (`endBrowserSession`), or make it real: ask HPAM to revoke the **refresh** token via Graph (`revokeSignInSessions`, or the token-revocation endpoint with the right credential), and treat failure to revoke as a reportable event rather than a swallowed log line. If revocation is HPAM's job, say so in the code, because right now this component reads as though it has already been done. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/teams-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-TM-05 — `getGraphServiceClient(token)` accepts a token argument and silently ignores it

| Finding `D-TM-05` | **Info** · no CVSS score recorded · component **Teams** |
|---|---|
| **The issue** | `getGraphServiceClient(token)` accepts a token argument that can never affect the request: it is **stored into `availableCredential`, which nothing on the request path reads**, because the graph client's auth provider returns `SecuredPreferences.accessToken` directly and the line that would have read it is commented out. |
| **Suggested fix** | Delete the ignored `token` parameter and its credential accessors, or re-enable the commented read at `AuthenticationManager.kt:16` — but not both silently. |
| **What was tested** | The **Teams** component, as provided in the source snapshot. The claim under test: *`getGraphServiceClient(token)` accepts a token argument and silently ignores it*. Artefacts read at the cited lines: `auth/AppAuthManager.kt:83,97` · `auth/AuthenticationManager.kt:14-17` (commented-out line at `:16`) |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed, mechanism restated** (§3.4.1). **Test record.** *[mechanism restated at verification 2026-09-08 — a severed read, not a dropped argument; effect unchanged]* |
| **How to resolve** | Delete the unused `token` parameter and `setMicrosoftCredential`/`getMicrosoftCredential` entirely, or re-enable the commented line at `AuthenticationManager.kt:16` — but not both silently. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/teams-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-TM-06 — A failed EULA/consent save proceeds into the application anyway

| Finding `D-TM-06` | **Info** · no CVSS score recorded · component **Teams** |
|---|---|
| **The issue** | A failed EULA/consent save proceeds into the application anyway |
| **Suggested fix** | Retry a failed consent save once, then either block entry or record a "consent not persisted" event that an operator will see. |
| **What was tested** | The **Teams** component, as provided in the source snapshot. Artefacts read at the cited lines: `ui/splash/SplashActivity.kt:280-286` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Distinguish the two: on failure, retry once, then either block or record a "consent not persisted" event that surfaces somewhere an operator sees. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/teams-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-TM-07 — No CI build or test workflow exists; the only automation on push is a secrets scan

| Finding `D-TM-07` | **Info** · no CVSS score recorded · component **Teams** |
|---|---|
| **The issue** | **No build or test gate on any change.** `release.yml` *is* a build workflow (`./gradlew assembleRelease`, producing `.hpk`), but it triggers only on `workflow_dispatch` and `v*` tags — never on push or PR — and runs **no test task of any kind**; `gitleaks.yml` is the only push/PR automation. The workflow that produces the distributed `.hpk` performs **no signing step** and pins `actions/checkout@v2` / `actions/setup-java@v1`. |
| **Suggested fix** | Adopt the sibling's `build.yml`, extend it to the release variant that actually ships, and run it on push and pull request. |
| **What was tested** | The **Teams** component, as provided in the source snapshot. The claim under test: *No CI build or test workflow exists; the only automation on push is a secrets scan*. Artefacts read at the cited lines: `.github/workflows/release.yml` · `.github/workflows/gitleaks.yml` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Partly refuted — the claim as written was false; band unchanged, text rewritten** (§3.4.1). **Test record.** *[PARTLY REFUTED and rewritten at verification 2026-09-08: the original "No CI build or test workflow" was false — a build workflow exists]* |
| **How to resolve** | Copy the sibling's `build.yml`. Add the release variant to it, since that is what ships. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/teams-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-CVL-01 — `isHPCloudUser()` and `isSIOEnabled()` are short-circuited to `false` by a hardcoded `if (true)`, making the suite's only trusted-agent check unreachable

| Finding `D-CVL-01` | **Medium** · CVSS 3.1 5.5 · component **CommonValueLibraryCypher** |
|---|---|
| **The issue** | `isHPCloudUser()` and `isSIOEnabled()` short-circuited by hardcoded `if (true) { return false; }` — the suite's only trusted-agent check (`isWhiteListedAgent()`, which calls `Principal.isAuthNAgentTrusted()`, one consumer in 32 components) is unreachable. Fails **closed** — deliberately scored Medium, not a privilege escalation; the class (an uncatchable two-line edit to a shared library) is the finding. |
| **Suggested fix** | Remove both `if (true)` short-circuits; if the capability is deliberately off for this fleet, express that as a named configuration flag, and add a unit test and a CI lint rule so it cannot recur. |
| **What was tested** | The **CommonValueLibraryCypher** component, as provided in the source snapshot. The claim under test: *`isHPCloudUser()` and `isSIOEnabled()` are short-circuited to `false` by a hardcoded `if (true)`, making the suite's only trusted-agent check unreachable*. Artefacts read at the cited lines: `sdk/WorkpathAccessService.java:109,138,147` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). **Test record.** **[verified 2026-09-08 — confirmed, and the reach is wider than first filed: `isSIOEnabled()` has 53 call sites and `isHPCloudUser()` 12 more across FIVE shipped components (CypherOneDrive, CypherSharePoint, Teams, MailFlow, UniversalPrint), all now permanently on the guest path. Fail-closed confirmed by sampling three `!isSIOEnabled()` branches in three different apps, not assumed. `isWhiteListedAgent()` has zero call sites outside the dead `:147`.]** |
| **How to resolve** | Remove both `if (true)` blocks. If these capabilities are deliberately disabled for the current fleet, express that as a named, documented configuration flag with a comment stating who disabled it and why — not as a constant condition that reads as a mistake. Add a unit test asserting each predicate's contract; add a lint rule (`ConstantConditions` / `SimplifiableConditional`) to CI and make it fail the build. Then decide, explicitly, whether `isAuthNAgentTrusted()` should be consulted somewhere — because right now it is not. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/commonvaluelibrarycypher-master.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-CVL-02 — A fully decrypted copy of a password-protected PDF is written next to the original and never deleted; the temp folder the caller supplies is ignored

| Finding `D-CVL-02` | **Low** *(was Medium 5.5)* · no CVSS score recorded · component **CommonValueLibraryCypher** |
|---|---|
| **The issue** | Fully decrypted, unrestricted copy of a password-protected PDF written **beside the original**; the caller-supplied `tempFolder` is declared and never read; **CVL never deletes the copy.** |
| **Suggested fix** | Write the decrypted copy into the `tempFolder` the caller already supplies, delete it in a `finally`, and prefer passing an open `ParcelFileDescriptor` so no plaintext file exists at all. |
| **What was tested** | The **CommonValueLibraryCypher** component, as provided in the source snapshot. The claim under test: *A fully decrypted copy of a password-protected PDF is written next to the original and never deleted; the temp folder the caller supplies is ignored*. Artefacts read at the cited lines: `print/view/preview/PdfPasswordHandler.kt:30,86,118` · sole caller `PrintSubPreviewFragment.java:252` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed, severity down (Medium to Low)** (§3.4.1). **Test record.** **[VERIFIED AND DOWN-SCORED 2026-09-08 — the open question is CLOSED. The print source is app-private internal storage in all four shipped consumers** (`CypherOneDrive utils/DirectoryHelper.java:59` · `CypherSharePoint DirectoryHelper.java:55` · `Teams util/DirectoryHelper.kt:17` · `MailFlow DirectoryHelper.kt:17`, all `Context.filesDir`)**, and all four print-preview activities are `exported="false"`, so no outside caller can redirect it. NOT High.** And **"never deleted anywhere in the 32-component frame" is REFUTED** — every host app deletes the whole app-data tree containing the file, at next launch or clean exit (`CypherOneDrive DirectoryHelper.java:180` via `SplashActivity.java:269,498` · `Teams util/Utils.kt:49 clearApp()` via `BaseActivity.kt:69`, `MainActivity.kt:295`). **What remains and is real:** the plaintext persists from preview until the app next terminates cleanly or relaunches — a crash or kill leaves it — readable by anything with shell, root or backup access to that app's data dir on a shared MFP. Fix is unchanged: honour `tempFolder`, delete after use.**]** |
| **How to resolve** | Write the decrypted copy into the `tempFolder` the caller already supplies (or `context.cacheDir`), delete it in a `finally` once the job completes or the activity is destroyed, and prefer passing an open `ParcelFileDescriptor` over a path so no plaintext file exists at all. Stop returning the plaintext password through the callback unless a caller demonstrably needs it — `PrintSubPreviewFragment.java:259` receives `usedPassword` and does not use it. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/commonvaluelibrarycypher-master.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-CVL-03 — The new shared `WebPageActivity` runs JavaScript in a WebView whose "allowed host" is taken from the very URL it was asked to load, and its abort path loads the page anyway

| Finding `D-CVL-03` | **Low** *(was Medium 5.0)* · no CVSS score recorded · component **CommonValueLibraryCypher** |
|---|---|
| **The issue** | New shared `WebPageActivity` runs JavaScript in a WebView whose origin allow-list derives from the very URL it was asked to load; no `shouldInterceptRequest`; abort path calls `finish()` **without returning**, so `loadUrl` still runs with `allowedHost` uninitialised. |
| **Suggested fix** | Pin `allowedHost` to a compile-time allow-list rather than to the input, add `shouldInterceptRequest`, turn JavaScript off, and add the missing `return` after `finish()`. |
| **What was tested** | The **CommonValueLibraryCypher** component, as provided in the source snapshot. The claim under test: *The new shared `WebPageActivity` runs JavaScript in a WebView whose "allowed host" is taken from the very URL it was asked to load, and its abort path loads the page anyway*. Artefacts read at the cited lines: `ui/webpage/WebPageActivity.kt:35,69-78,114-129` · gate settled at `MailFlow model/ErrorData.kt` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed, severity down (Medium to Low)** (§3.4.1). **Test record.** **[VERIFIED AND DOWN-SCORED 2026-09-08 — the gating question is CLOSED. MailFlow's `error.codeLink` is a compile-time constant:** `ErrorData` is constructed in exactly two places, both companion factories in `model/ErrorData.kt:14-20,22-28`, each hardcoding the same `help.hpauthsuite.com` literal; no other `ErrorData(` exists in the app. **The activity's other caller (`ui/dialog/LinkTextDialogFragment.kt:21`) forwards `URLSpan` URLs out of string resources — also constant — and the activity is `exported="false"` in CVL's library manifest (`:17-21`). No path in this snapshot reaches this WebView with attacker-influenced input.** The code defects are real and should still be fixed; they are latent, not live.**]** |
| **How to resolve** | Pin `allowedHost` to a compile-time allow-list, not to the input. Add `shouldInterceptRequest` and apply the same predicate to sub-resources. Turn JavaScript off — the only JS the class needs is its own `PREVENT_TEXT_SELECTION_JS` (`:134-149`), which is cosmetic and can be a CSS injection at load or dropped. Add `return` after `finish()` at `:75`, and make `allowedHost` non-`lateinit` with a safe default. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/commonvaluelibrarycypher-master.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-CVL-04 — The siblings link three different versions of this library, by two different distribution mechanisms

| Finding `D-CVL-04` | **Info** · no CVSS score recorded · component **CommonValueLibraryCypher** |
|---|---|
| **The issue** | Three CVL versions in play by two distribution mechanisms (source 1.09.09; CypherOneDrive vendors 1.09.09 as a checked-in binary outside SCA; Teams resolves 1.09.06 remotely, two patches behind); no manifest says what the fleet runs |
| **Suggested fix** | Publish CVL to one internal Maven repository, pin every consumer to the same version, and remove the vendored `.aar` from `CypherOneDrive-main`. |
| **What was tested** | The **CommonValueLibraryCypher** component, as provided in the source snapshot. The claim under test: *The siblings link three different versions of this library, by two different distribution mechanisms*. Artefacts read at the cited lines: `build.gradle.kts:12` · `CypherOneDrive-main/CVL/*.aar` · `Teams-main/app/build.gradle.kts:151` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). |
| **How to resolve** | Publish CVL to one internal Maven repository, pin every consumer to the same coordinate and version, remove the vendored `.aar` from `CypherOneDrive-main`, and add a dependency-report check to CI. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/commonvaluelibrarycypher-master.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-CC-01 — The Android SDK hex-dumps plaintext APDUs — including the enroll-code verification command — to the log in release builds, because the app never turns verbose output off; iOS does

| Finding `D-CC-01` | **High** · CVSS 3.1 7.1 · component **Cyphercard-Enrolment-App** |
|---|---|
| **The issue** | Android **release** builds hex-dump plaintext APDUs — incl. the card's management-PIN verification command — to the log before encryption (verbose default `true`, never overridden, no minify); iOS turns the same flag off. |
| **Suggested fix** | Pass `isDebugOutputVerbose = false` at `SentrySdk.android.kt:27`, as iOS already does one file over, and stop logging APDU payloads at all. |
| **What was tested** | The **Cyphercard-Enrolment-App** component, as provided in the source snapshot. The claim under test: *The Android SDK hex-dumps plaintext APDUs — including the enroll-code verification command — to the log in release builds, because the app never turns verbose output off; iOS does*. Artefacts read at the cited lines: `api/BaseApi.kt:33,80-84` · `api/BiometricsApi.kt:555-560` · `sdk/SentrySdk.kt:32` · **`sdk/SentrySdk.android.kt:27`** · `composeApp/build.gradle.kts:95` · `NativeSdkBridgeImpl.swift:18` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). **Test record.** **[verified 2026-09-08 — confirmed; the decisive line is the OMISSION at `SentrySdk.android.kt:27`, which constructs the SDK without passing `isDebugOutputVerbose` and so takes the `true` default, where iOS passes `false`. `log()` is `println` gated only on that flag (`BaseApi.kt:80-84`), and release strips nothing (`composeApp/build.gradle.kts:95`, `isMinifyEnabled = false`).]** |
| **How to resolve** | Pass `isDebugOutputVerbose = false` at `SentrySdk.android.kt:27`, matching what iOS already does one file over. Independently, in the vendored SDK, stop logging APDU payloads at all — or log only command headers, never data — because a debug flag is the wrong last line of defence for a credential. Turn on `isMinifyEnabled` with `-assumenosideeffects` for `println`/`Log` as defence in depth. Address the `//todo disable logs for release builds` at `composeApp/src/commonMain/.../di/AppModule.kt:41`, which sets the app's own Kermit logger to `minSeverity = Severity.Debug` (`:45`) — a second, independent debug-logging default. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cyphercard-enrolment-app-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-CC-02 — One hardcoded six-digit code authorises fingerprint enrolment and full reset on every card in the estate, and enrolment deliberately leaves the card unlocked afterwards

| Finding `D-CC-02` | **High** · CVSS 3.1 7.2 · component **Cyphercard-Enrolment-App** |
|---|---|
| **The issue** | One hardcoded six-digit code (authors' own `// fixme change default code`) authorises fingerprint enrolment and full reset on every card, and enrolment deliberately leaves the card unlocked (`lockOnEnrollComplete = false`). Final chain link (re-enrolled card still authenticates as its original owner) reasoned from architecture, **not verified in HPAM** |
| **Suggested fix** | Set `lockOnEnrollComplete = true`, stop shipping the enrol code in the binary, and plan on the basis that the current card population is already compromised. |
| **What was tested** | The **Cyphercard-Enrolment-App** component, as provided in the source snapshot. The claim under test: *One hardcoded six-digit code authorises fingerprint enrolment and full reset on every card in the estate, and enrolment deliberately leaves the card unlocked afterwards*. Artefacts read at the cited lines: `config/Config.kt:4-5` · `SentrySdk.android.kt:52` (and `:27`) · `SentrySDK.swift:43` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). **Test record.** **[verified 2026-09-08 — confirmed; precise anchor is `Config.kt:4-5` (the authors' `// fixme` comment at `:4`, the declaration at `:5`), and the code's own comment at `SentrySdk.android.kt:46-47` states that `lockOnEnrollComplete = true` would prevent further enroll/delete, so leaving it false is deliberate. The unverified final chain link is unchanged — it needs a card and a live HPAM.]** |
| **How to resolve** | Three separable changes, in priority order. (1) Set `lockOnEnrollComplete = true` — the SDK already supports it and the code comments already describe it; if re-enrolment must remain possible, gate it behind an operator credential that is not the card's own management PIN. (2) Stop shipping the enroll code in the binary: source it from operator input, a provisioning profile, or a keystore-backed secret, and personalise cards with per-batch (ideally per-card) codes. (3) Treat the current population as compromised for planning purposes — the code is in a repository, in every APK, and in the log (D-CC-01) — and decide whether re-personalisation is required before a defence deployment. **That last decision is Kam's and the client's, not this review's.** *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cyphercard-enrolment-app-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-CC-03 — `android:allowBackup="true"` on an app whose whole purpose is card provisioning

| Finding `D-CC-03` | **Low** · CVSS 3.1 2.4 · component **Cyphercard-Enrolment-App** |
|---|---|
| **The issue** | `android:allowBackup="true"` on the card-provisioning app — **one of three** that set it true (the others: `myPKI MauiAppTutor/Platforms/Android/AndroidManifest.xml:3`, `QuickAccessLibrary app/src/main/AndroidManifest.xml:5`), not "the only one". |
| **Suggested fix** | Set `android:allowBackup="false"`, matching the ten manifests in the estate that already do. |
| **What was tested** | The **Cyphercard-Enrolment-App** component, as provided in the source snapshot. The claim under test: *`android:allowBackup="true"` on an app whose whole purpose is card provisioning*. Artefacts read at the cited lines: `composeApp/src/androidMain/AndroidManifest.xml:15` |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Verdict for this row: Confirmed as filed** (§3.4.1). **Test record.** *[denominator corrected at verification 2026-09-08: three of the **14** manifests that set the attribute at all; **31** `AndroidManifest.xml` files exist in the tree — the earlier "of twelve" does not reproduce]* |
| **How to resolve** | Set `android:allowBackup="false"`, matching the ten manifests that already do. One line. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cyphercard-enrolment-app-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 3.4.1 Per-finding verification verdicts

| Verdict | IDs |
|---|---|
| **Confirmed as filed** (17) | D-OD-01 · D-OD-02 · D-OD-03 · D-OD-04 · D-OD-05 · D-OD-07 · D-OD-08 · D-TM-01 · D-TM-02 · D-TM-03 · D-TM-04 · D-TM-06 · D-CVL-01 · D-CVL-04 · D-CC-01 · D-CC-02 · D-CC-03 |
| **Confirmed, mechanism or wording restated** (2) | D-OD-06 · D-TM-05 |
| **Confirmed, SEVERITY DOWN** (2) | D-CVL-02 (Medium to Low) · D-CVL-03 (Medium to Low) |
| **Confirmed in part — aggravator refuted** (1) | D-MF-07 (§2.3.2; band unchanged at Low) |
| **Partly refuted — claim as written was false** (1) | D-TM-07 (band unchanged at Info; text rewritten) |
| **Refuted outright** | *none* |
| **Moved up** | *none* |

**Three findings were strengthened without moving band:** `D-CVL-01`, where the reach is
fifty-three plus twelve call sites across five shipped components with fail-closed confirmed by
sampling; `D-CC-01`, where the decisive omission line was identified at `SentrySdk.android.kt:27`;
and `D-OD-01`, where the endpoint was traced to the printer's Workpath solution configuration,
validated only for non-emptiness at `CloudConfigExtensions.kt:6`.

**Two severity-gating questions that this section carried open are now closed, and both close
downward.** They were open because two filing sessions were honest enough to state what they had
assumed rather than resolve it by preference. Both were settled at source, and neither needed a live
system.

1. **The CommonValueLibraryCypher print-source storage location: closed, app-private.** All four
 shipped consumers of the print-preview path put the source file in `Context.filesDir`, and all
 four print-preview activities are `exported="false"`. `D-CVL-02` does not rescore to High; it
 rescores down to Low, and its "never deleted" clause is refuted by the host applications' own
 cleanup.
2. **The origin of MailFlow's `error.codeLink`: closed, a compile-time constant**, hardcoded
 identically in the only two `ErrorData` factories that exist. `D-CVL-03` does not rescore upward;
 it rescores down to Low.

**What this pass did not test, stated so that "verified" is not over-read.** No CVSS arithmetic, since
no vectors are recorded. Nothing live: the tenant question is unresolved and the live pass is held, so
every conclusion of the form "not externally reachable" or "app-private" is static and about this
snapshot. No vendored archive was decompiled. `D-CC-02`'s final chain link still needs a card and a
live HPAM instance.

**One item was opened and left open rather than filed.** HPAM's own separate `WebPageActivity` has no
host allow-list at all, with JavaScript and DOM storage enabled. It is `exported="false"`, but the
origin of its `status.errorLink` input was not traced. It is not filed, because this pass does not
file what it has not tested.

**Also carried from that batch and not re-litigated here:** four June component summaries are stale on
authentication and attestation architecture — `cypheronedrive`, `teams-main` and
`commonvaluelibrarycypher`, one claim of which is actively inverted — and should be regenerated
before being quoted to a customer. `cyphercard-enrolment-app` remains substantially accurate.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.5 Bearer-scheme sweep

Batch 2 flagged the missing-`Bearer`-scheme defect as *"very likely also in CypherSharePoint,
MailFlow and UniversalPrint, not checked."* It was checked on 2026-09-08 by construction shape rather
than by the word, with a positive control that found both known instances before any zero was
believed, plus a constant-consumer sweep for the map-index syntax that the shape search cannot see.

- **CypherSharePoint: clean.** All seven `Authorization` lines are schemed; its
`QuickAccessPresenter.kt:112` carries `"Bearer $token"`, so the sibling fixed the shared shape.
- **UniversalPrint: clean.** All twenty-five lines are schemed.
- **MailFlow: the defect is confirmed at seven sites**, giving one new finding.

**Summary of the findings in this section.** The full record for each — the issue, the suggested fix, and below them what was tested, how it was tested and how to resolve it — follows the table, one finding to a block.

| ID | Component | Severity | CVSS 3.1 | Finding |
|---|---|---|---|---|
| D-MF-07 | MailFlow | Low | 3.1 | Seven MailFlow HTTP sites send the raw access token with no `Bearer` scheme — the same shared-code defect as CypherOneDrive/Teams, but on the primary… |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-MF-07 — Seven MailFlow HTTP sites send the raw access token with no `Bearer` scheme — the same shared-code defect as CypherOneDrive/Teams, but on the primary mail/attachment/PDF paths, and one site sends it to a server-designated URL

| Finding `D-MF-07` | **Low** · CVSS 3.1 3.1 · component **MailFlow** |
|---|---|
| **The issue** | Seven sites send the raw access token with no `Bearer` scheme (six Graph sites via `getGraphAccessToken()` on the mail/attachment/PDF paths; the correct helper exists in the same app and is used at five other sites). ~~**Aggravator:** the seventh site sends the raw credential to a URL designated by the Gotenberg service~~ — **STRUCK at verification 2026-09-08.** The seventh site (`GotenbergCloudRenderingRequestJob.kt:250-253`) is in a class **nothing in MailFlow constructs**, and `contentLocation` is a **caller-supplied input** field, not a service-designated one. **No rescore: Low stands** on the six live Graph sites, where an unschemed token is a request Microsoft rejects — a functional defect with no exposure. Detail below the table |
| **Suggested fix** | Use the `Bearer`-prefixing helper that already exists in the same application at the six live Graph sites; the seventh site is in a class nothing constructs and should be deleted with the rest of that dead code. |
| **What was tested** | The **MailFlow** component, as provided in the source snapshot. The claim under test: *Seven MailFlow HTTP sites send the raw access token with no `Bearer` scheme — the same shared-code defect as CypherOneDrive/Teams, but on the primary mail/attachment/PDF paths, and one site sends it to a server-designated URL*. Artefacts read at the cited lines: `microsoft/download/MicrosoftGraphPdfDownloadProviderImpl.kt:443,466,495,515,537,656,755-757` · `GotenbergCloudRenderingRequestJob.kt:82,250-253` |
| **How it was tested** | Static, read-only source review of the provided snapshot, by construction shape rather than by the word, with a positive control that found both known instances before any zero was believed, plus a constant-consumer sweep for the map-index syntax that the shape search cannot see. **No per-row test record was written for this row**, so the section method above is the whole of what can be said about how it was tested. That is stated rather than filled in. |
| **How to resolve** | Route the six live Graph sites through the helper that already prefixes the scheme correctly at five other sites in the same application, rather than constructing the header by hand. Delete `GotenbergCloudRenderingRequestJob` and the rest of the unreachable cloud-rendering path. **Deleting that dead class does not discharge the credential it carries:** the Entra client-secret-class value at `GotenbergCloudRenderingRequestJob.kt:39` is already Critical #12 and F-16, it is present in released application packages, and it still requires rotation. |

**Why the aggravator was struck, in full, because the register carried it as an open severity
question.**

1. **`contentLocation` is not service-designated; the register had the wrong field.** In the
`cloudrendering` library's own model (`CloudRenderingJobItem.java:7-43`), `contentLocation` is an
**input** set by the caller in all three constructors and by `setContentLocation`. The field the
 service designates is a different one on a different class, `JobStatus.java:24
 outputContentLocation`.
2. **The site is unreachable in this snapshot.** A search for `GotenbergCloudRenderingRequestJob`
 across `MailFlow-main` returns two hits, the class declaration at `:29` and its own `TAG` at
`:35`. **Nothing constructs it.** The wired provider is `MicrosoftGraphPdfDownloadProviderImpl`,
 set at `provider/ServiceProviderManager.kt:83`. This project already knew: the batch-1 MailFlow
 delta file recorded it on 2026-09-07. The sweep filed the aggravator without that context.
3. **What does not go away.** The Entra client-secret-class credential in that same dead class
 (`GotenbergCloudRenderingRequestJob.kt:39`, reported structurally, value never copied) is already
Critical #12 and F-16, and still requires rotation. Deleting dead code does not un-ship a
 credential that is already in released application packages.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.6 Delta review, batch 1 — seven June-baseline components

Sixty-two findings in seven identifier series, measured by counting finding headings and their
severity lines across the seven batch-1 delta files, rather than estimated. The commissioning brief
had estimated *"roughly twenty"*.

**Verification status: all sixty-two rows have been independently re-derived at source.** Round 2
covered this section in three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from
the specification and validated it against published reference vectors **before** scoring, and each
re-derived the vector from source metric by metric rather than recomputing the filed one. **Severities
and scores below are not transcribed; they are re-derived, and the vector is recorded beside the score
wherever a verifier produced one.** Rows are left in their original order, so the table is not sorted
by severity within a component: read the severity cell, not the position.

**`D-MF-01` is withdrawn and is no longer counted, and the row is still printed below, deliberately.**
A withdrawal is not a deletion: the row keeps its evidence and the measurement that refuted it, and
only its place in the count changes. **`D-UP-07` is new**, filed on the same ruling. **So this table
prints sixty-three rows and the tally counts sixty-two.** That is the intended state, and the extra
row is the withdrawn one.

**Cross-component duplicates, flagged so that the total is not read as sixty-two distinct defects.**
The per-component convention is preserved, each component counting its own findings, but three
defects appear more than once. LicenseServer `NEW-1` is the reviewer's own declared mirror of
License-Services `NEW-1`: one forgeable licensing decision, two products. The disabled OnGuardLib
application-integrity gate is `D-MF-06`, `D-SP-03` and `D-UP-05`: one control, three applications.
The inert gitleaks rollout is `I-D9` and `H-D7`. Counting them per component matches how F-13 and
F-16 are already handled estate-wide. **Deduplicated, the sixty-two rows represent fifty-eight
distinct defects.**

**Summary of the findings in this section.** The full record for each — the issue, the suggested fix, and below them what was tested, how it was tested and how to resolve it — follows the table, one finding to a block.

| ID | Component | Severity | CVSS 3.1 | Finding |
|---|---|---|---|---|
| D-MF-01 | MailFlow | **WITHDRAWN 2026-09-09** *(was High)* | **n/a — withdrawn; the filed 7.5 is void** | Microsoft Graph service root and OAuth authority are taken verbatim from HPAM-supplied remote config, with no host allow-list, and the user's Entra bearer… |
| D-MF-02 | MailFlow | Medium | 5.4 | Inbound HTML e-mail bodies are rendered in a JavaScript-enabled WebView with no sanitisation and no sub-resource filtering |
| D-MF-03 | MailFlow | Medium | 4.7 `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N` | The "release" predicate excludes the `releaseautotest` build type, so a release-signed, shipped variant re-enables WebView remote debugging and screen… |
| D-MF-04 | MailFlow | Medium | **5.3** `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:H/A:N` | Admin-consent OAuth request carries no `state` parameter (dead statement), and the tenant id is harvested from the redirect URL and persisted with no binding |
| D-MF-06 | MailFlow | Medium | 6.2 | OnGuardLib native app-integrity gate is disabled: `isApplicationAuthorized` returns hardcoded `true` |
| D-MF-05 | MailFlow | Low | 3.1 | `EnableSafeBrowsing` meta-data is declared outside `<application>` and is therefore inert |
| D-SP-01 | CypherSharePoint | **High** | 7.5 `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` | The Graph service root is taken verbatim from HPAM-supplied remote config, and `AuthInterceptor` attaches the user's Entra bearer token to every request on… |
| D-SP-02 | CypherSharePoint | **Low** | **3.3** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` | Microsoft Graph SDK logger is wired at `LoggerLevel.DEBUG` into the live Graph client, and the whole cloud config is logged |
| D-SP-03 | CypherSharePoint | Medium | 6.2 | The OnGuard native locker in the SharePoint APK ships OAuth/vault credential sets for six cloud providers, only one of which the app uses — and the gate… |
| D-SP-04 | CypherSharePoint | Low | **3.6** `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:N` | The custom permission that guards the HPAM token IPC is declared with no `protectionLevel` (defaults to `normal`), and the app declares it without requesting it |
| D-SP-05 | CypherSharePoint | Info | — | Outbound e-mail falls back to the network host name as the `From` address |
| I-D1 | infra_hpam | **Critical** | **9.1** `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` | Mutable shared container tag: any repository writer can overwrite the exact image all four production Keycloak instances run |
| I-D2 | infra_hpam | **Critical** | **9.9** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` | Terraform is the mechanism that keeps regenerating the F-16 master credentials, and the App Services cannot stop using them |
| I-D10 | infra_hpam | Medium | **n/a — posture finding** | No network isolation is deployed anywhere in the topology; the only boundary code in the repository is the commented-out `modules/vnet` |
| I-D11 | infra_hpam | Medium | 6.5 `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` | The app-registration alert container bakes a tenant-wide service-principal credential into an image layer and passes it on the `az` command line |
| I-D3 | infra_hpam | Medium | 5.3 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N` | Keycloak trusts a client-supplied `Forwarded` header: the CLI proxy-header setting overrides the app setting, and Azure App Service does not sanitise that… |
| I-D4 | infra_hpam | Medium | **5.9** `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:N` | The Keycloak database is in public-access mode with its firewall managed by hand, outside Terraform, per the project's own runbook |
| I-D5 | infra_hpam | Medium | 5.9 `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:N` | All three App Service modules leave `ftps_state` at the `AllAllowed` default, exposing a plaintext FTP publishing endpoint on the identity provider and the… |
| I-D6 | infra_hpam | Medium | 4.3 `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` | Production has no security telemetry: zero diagnostic settings, no authentication-failure alerting, and detailed error messages plus failed-request tracing… |
| I-D7 | infra_hpam | Medium | 5.3 `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N` | The cryptographic `SALT` for the HPAM API is generated by `random_string`, not `random_password`: it is non-sensitive, printed in plan output, and stored in… |
| I-D9 | infra_hpam | Medium | **n/a — posture finding** | The estate-wide gitleaks rollout is inert: 25 repositories now run a secret-scanning workflow, and every one of them pins a version of `actions/checkout`… |
| I-D8 | infra_hpam | **Medium** | **5.4** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` | Dev, staging and demo telemetry is hardwired into the production Log Analytics workspace |
| NEW-1 | License-Services | **Critical** | **10.0** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` | The licensing decision is forgeable without the root CA key: the tenant signing key ships inside every licence, wrapped to a key committed in cleartext, and… |
| NEW-2 | License-Services | **Medium** | **6.5** `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:H/A:H` | Loading the Tenants page permanently deletes the licence record of every tenant whose licence fails validation, including every expired licence — and… |
| NEW-3 | License-Services | Medium | 5.3 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` | Anonymous, internet-facing customer enumeration: `/api/validate` discloses which Azure AD tenants are HP Authentication Suite licensees |
| NEW-4 | License-Services | Medium | **6.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L` | Every authenticated user of every Azure AD tenant on earth is a full licensing administrator for their own tenant: no role, group or app-role check exists… |
| NEW-5 | License-Services | **High** | **7.1** `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` | Cross-tenant super-admin is granted by an unanchored substring regex over the user's UPN |
| NEW-8 | License-Services | Medium | 5.9 `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N` | The committed private-key inventory is larger than recorded, and the artefacts missing from it are exactly the ones text-pattern scanning cannot see —… |
| NEW-10 | License-Services | Low | **3.3** `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:N` | `Jose.JWT.Decode` is called with no expected algorithm, in the one place the sibling implementation constrains it |
| NEW-6 | License-Services | **Medium** | 4.7 `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N` | Security headers never reach unauthenticated or static responses: `SecurityHeadersMiddleware` is registered after the two middlewares that short-circuit |
| NEW-7 | License-Services | Low | 3.7 `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N` | The tenant-selection session cookie is created with framework defaults (not `Secure`, not `SameSite=Strict`, id never regenerated at sign-in), and the one… |
| NEW-9 | License-Services | Low | **3.9** `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` | Certificate issuance under the licensing root has no extensions, uses predictable serial numbers in both C# generators, and accepts DN injection from a… |
| NEW-11 | License-Services | Info | — | No `ValidAlgorithms` allow-list on any JWT validator |
| NEW-12 | License-Services | Info | — | Security-through-obscurity is a documented practice here |
| NEW-13 | License-Services | Info | — | LIKE-wildcard injection in the device serial filter |
| NEW-14 | License-Services | Info | — | Documentation asserts controls the code does not implement |
| H-D1 | HPK_Deployment_Utility | **High** | **8.6** `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` | Unsigned, unauthenticated job-manifest import is a supply-chain channel into the printer fleet; `ValidateHpkFile` is a metadata extractor whose name asserts… |
| H-D2 | HPK_Deployment_Utility | **Low** | **3.3** `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N` | Arbitrary file write with fully attacker-controlled content: the manifest's `Hpk.FileName` reaches `Path.Combine` and `File.WriteAllBytesAsync` unsanitised |
| H-D5 | HPK_Deployment_Utility | **High** | **8.8** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` | The Worker's unauthenticated control plane is the SQLite database and the `hpks/` staging folder, not the stop-signal |
| H-D3 | HPK_Deployment_Utility | Medium | **6.1** `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` | Argument injection with a new external taint source: `--uuid` is interpolated unquoted from the attacker-supplied `hpk.xml` |
| H-D4 | HPK_Deployment_Utility | Medium | **4.7** `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N` | The LDB service key is written to the error log in cleartext |
| H-D6 | HPK_Deployment_Utility | Medium | **6.5** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` | Debug symbols are hidden rather than removed from the release archive, and every push to `main` publishes the binary that carries the F-15 hardcoded AES key |
| H-D7 | HPK_Deployment_Utility | Medium | **n/a — control failure** | The estate-wide gitleaks rollout is inert: this repository's secret-scanning workflow pins a version of `actions/checkout` that does not exist |
| H-D8 | HPK_Deployment_Utility | Low | **n/a — assurance finding** *(computes 2.5)* | Silence from `HPKTool-cli.exe` is recorded as a successful deployment |
| H-D9 | HPK_Deployment_Utility | Low | **3.6** `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:L` | `SettingsUtils.AppSettings` fires an `async void` load from a property getter, so the first read can silently return empty credentials |
| NEW-1 | LicenseServer | **Critical** | **10.0** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` | The licensing decision is forgeable without the root CA key (mirror of `license-services-main.md` NEW-1, as it manifests here) |
| NEW-2 | LicenseServer | **High** | **8.7** `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` | One private key serves three different purposes across two independently-deployed products: TLS server key, LicenseServer JWE key, and License.Portal JWE key |
| NEW-3 | LicenseServer | **High** | 7.5 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` | The root CA private key is committed as a compiled binary, so deleting the `.key` file does not remove it from the repository — and the Dockerfile bakes the… |
| NEW-4 | LicenseServer | **High** | 7.5 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` | There is no revocation mechanism of any kind, and the unauthenticated `/upload` makes licence state actively rollback-able: an old, more generous licence… |
| NEW-5 | LicenseServer | **High** | **8.6** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` | The licence's own `tenantId` claim is never read: a licence issued for one tenant can be installed as another tenant's licence, and is never re-checked at… |
| NEW-6 | LicenseServer | Medium | **n/a — architectural aggregate, not additive** *(own vector computes 7.3; DO NOT ADOPT)* | Two divergent implementations of one licensing protocol share one root CA and one key, so the system's security is that of the weaker implementation |
| NEW-7 | LicenseServer | Medium | **6.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L` | EOL runtime, beyond the version number: floating package ranges with no lock file on an unsupported feed, an unpatchable base image rebuilt on every push,… |
| NEW-8 | LicenseServer | Medium | 5.3 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` | This repository has no secret-exclusion policy and no secret scanning at all, while its sibling has both |
| NEW-9 | LicenseServer | **Medium** | **4.6** `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:N` | Generator hygiene: no operator authentication, no minting audit, predictable certificate serials, no certificate extensions, DN injection, no transport… |
| NEW-10 | LicenseServer | Info | — | What the committed sample licence tells us, and what it does not |
| NEW-11 | LicenseServer | Info | — | No `ValidAlgorithms` allow-list |
| D-UP-01 | UniversalPrint | **Informational** | **n/a — latent, no reachable path** | The shared "hardened auth WebView" helper enables remote WebView debugging unconditionally, including on the WebView into which plaintext Entra admin… |
| D-UP-02 | UniversalPrint | **Informational** | **n/a — latent, no reachable path** | The auth-WebView origin allow-list returns `true` for `javascript:`, `data:`, `blob:` and `about:` URIs before it applies the HTTPS/host test |
| D-UP-03 | UniversalPrint | Medium | 4.2 | IPP certificate "pinning" derives its trust anchor from an unauthenticated fetch performed by a deliberately obfuscated trust-all TrustManager |
| D-UP-04 | UniversalPrint | Medium | **5.3** `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:H/A:N` | Admin-consent OAuth request carries no `state` parameter (dead statement), and the tenant id is harvested from the redirect URL and persisted with no binding |
| D-UP-05 | UniversalPrint | Medium | 6.2 | OnGuardLib native app-integrity gate is disabled: `isApplicationAuthorized` returns hardcoded `true`, and four of six JNI call-sites are additionally… |
| D-UP-06 | UniversalPrint | Low | — | Cross-cutting: five divergent private forks of OnGuardLib, which is why the same control is enabled in two apps and disabled in three |
| D-UP-07 | UniversalPrint | Medium | **n/a — control absence; no off-origin navigation path established** | All three auth WebViews run with JavaScript enabled and have no origin allow-list and no sub-resource filtering at all — including the one that receives the… |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-MF-01 — Microsoft Graph service root and OAuth authority are taken verbatim from HPAM-supplied remote config, with no host allow-list, and the user's Entra bearer token is sent to whatever host that config names

| Finding `D-MF-01` | **WITHDRAWN 2026-09-09** *(was High)* · CVSS 3.1 **n/a — withdrawn; the filed 7.5 is void** · component **MailFlow** |
|---|---|
| **The issue** | Microsoft Graph service root and OAuth authority are taken verbatim from HPAM-supplied remote config, with no host allow-list, and the user's Entra bearer token is sent to whatever host that config names |
| **Suggested fix** | **Withdrawn — no remediation attaches to this row.** The defect the evidence actually describes is `D-SP-01` in CypherSharePoint, which is unaffected, still counted, and carries the fix. |
| **What was tested** | The **MailFlow** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/mailflow-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[REFUTED OUTRIGHT 2026-09-09, `round2-c.md` §2.1 — AND STILL COUNTED, DELIBERATELY.** The premise is absent from this component: `CloudConfig` appears **zero** times in the `MailFlow-main` tree (positive control, same command form: `GraphServiceClient` returns 63), every cited `MSAppAuthHelper.kt` line is a different function, and every endpoint in the app is a compile-time literal (`MSConstants.kt:7,10`; `MicrosoftMainProviderImpl.kt:83`). The verifier's diagnosis is **transposition**: this is `D-SP-01`'s evidence re-filed against a component that does not have the defect. **WITHDRAWN 2026-09-09 on Tuesday's ruling — §2.3.7 open item 1a, ACCEPT as a MARKED WITHDRAWAL.** **THE ROW IS NOT DELETED AND MUST NOT BE.** It stays in this register, marked withdrawn, **carrying the measurement that refuted it**, and it comes out of the counted total and out of the severity tallies only — estate Highs −1. A reader must be able to see that a finding was raised, tested and withdrawn, and why: **the withdrawal reasoning above is itself the evidence of rigour, and a register that quietly loses rows is one nobody can audit.** **What is withdrawn is this row, not the defect.** Seat C's diagnosis is transposition, so the underlying defect still exists where the evidence actually came from — **`D-SP-01` in CypherSharePoint, which is unaffected, still counted and still stands.**] |
| **How to resolve** | Constrain `graphApi` / `oAuthAuthority` to a compiled-in allow-list of Microsoft national-cloud hosts (as UniversalPrint does for its four clouds in `remoteconfig/PrintCloudConfig.kt:19,29,39,49`) and reject anything else; additionally, refuse to attach the Authorization header to any host outside that list at the interceptor layer. **Not checked:** the HPAM `cloudconfig` AAR itself (closed-source, out of this component); whether the config channel is signature-protected on HPAM's side. `[GAP]` *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/mailflow-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-MF-02 — Inbound HTML e-mail bodies are rendered in a JavaScript-enabled WebView with no sanitisation and no sub-resource filtering

| Finding `D-MF-02` | **Medium** · CVSS 3.1 5.4 · component **MailFlow** |
|---|---|
| **The issue** | Inbound HTML e-mail bodies are rendered in a JavaScript-enabled WebView with no sanitisation and no sub-resource filtering |
| **Suggested fix** | Turn JavaScript off on the mail-body WebView, sanitise with a Jsoup `Safelist` before loading, and block remote sub-resources with `shouldInterceptRequest`. |
| **What was tested** | The **MailFlow** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/mailflow-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed exactly. Sanitisation census: `Jsoup` appears 3 times, **all `Jsoup.parse`; zero `Jsoup.clean`, zero `Safelist`, zero `Whitelist`**. The reviewer's own bounding — opaque origin, no file access, no JS bridge, so the token is not reachable from page script — is honest and correct, and it is what keeps `C:L/I:L` rather than higher. *(Contrast `:138`, where the same class sets `javaScriptEnabled = false` on another WebView — the team knows the setting.)*]* |
| **How to resolve** | Set `javaScriptEnabled = false` on the body WebView (it renders static mail, it does not need JS); failing that, sanitise with a Jsoup `Safelist` before `loadDataWithBaseURL`, add a restrictive CSP `<meta>`, and add `shouldInterceptRequest` to block all remote sub-resources by default. **Not checked:** whether the printer firmware's WebView implementation applies its own remote-content policy. `[GAP]` *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/mailflow-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-MF-03 — The "release" predicate excludes the `releaseautotest` build type, so a release-signed, shipped variant re-enables WebView remote debugging and screen capture; the correct predicate exists and is never used

| Finding `D-MF-03` | **Medium** · CVSS 3.1 4.7 `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N` · component **MailFlow** |
|---|---|
| **The issue** | The "release" predicate excludes the `releaseautotest` build type, so a release-signed, shipped variant re-enables WebView remote debugging and screen capture; the correct predicate exists and is never used |
| **Suggested fix** | Replace every `isReleaseMode` guard on a security decision with `isProductionMode`, and remove the `*autotest` build types from release signing. |
| **What was tested** | The **MailFlow** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/mailflow-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: score confirmed. The finding's stated positive control is **refuted and the defect is wider** — `isProductionMode` has **four** call sites (`SplashPresenter.kt:86`, `GoogleDownloadProviderImpl.kt:381`, `MicrosoftDownloadProviderImpl.kt:277`, `Constants.kt:51`), not zero: the correct predicate was understood and applied elsewhere, just not to the security guards. And there are **four** `isReleaseMode` guard sites, not three.]* |
| **How to resolve** | Replace every `isReleaseMode` guard around a *security* decision with `isProductionMode` (or, better, `!BuildConfig.DEBUG` plus an explicit hardening flag), and delete the `*autotest` build types from release-signing. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/mailflow-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-MF-04 — Admin-consent OAuth request carries no `state` parameter (dead statement), and the tenant id is harvested from the redirect URL and persisted with no binding

| Finding `D-MF-04` | **Medium** · CVSS 3.1 **5.3** `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:H/A:N` · component **MailFlow** |
|---|---|
| **The issue** | Admin-consent OAuth request carries no `state` parameter (dead statement), and the tenant id is harvested from the redirect URL and persisted with no binding |
| **Suggested fix** | Generate, assign, persist and check a cryptographically random `state` on the admin-consent request, and add an origin allow-list to that WebView. |
| **What was tested** | The **MailFlow** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/mailflow-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: `C:L` to `C:N` at source — nothing is disclosed; the defect is integrity of the tenant binding, and the OAuth authority is a resource constant. 4.7 to 5.3, band unchanged.]* |
| **How to resolve** | Generate a cryptographically random `state`, **assign** it into `queryParams`, persist it for the duration of the flow, and reject any redirect whose `state` does not match. Add an origin allow-list to this WebView (reuse UniversalPrint's `isAllowedAuthUri` approach, with the `javascript:`/`data:` exemption removed — see `universalprint-main.md` D-UP-02). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/mailflow-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-MF-06 — OnGuardLib native app-integrity gate is disabled: `isApplicationAuthorized` returns hardcoded `true`

| Finding `D-MF-06` | **Medium** · CVSS 3.1 6.2 · component **MailFlow** |
|---|---|
| **The issue** | OnGuardLib native app-integrity gate is disabled: `isApplicationAuthorized` returns hardcoded `true` |
| **Suggested fix** | Restore the gate call at `auth.cpp:10` and implement F-13's signature check inside `isApplicationPackageGenuine`. |
| **What was tested** | The **MailFlow** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/mailflow-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed exactly — same `auth.cpp:8-12` disabled gate, live call sites in `locker.cpp`.]* |
| **How to resolve** | Restore the call at `auth.cpp:10`, *and* implement F-13's signature check inside `isApplicationPackageGenuine`. Verify by asserting `isApplicationAuthorized` returns `false` for an unauthorised caller, not by inspecting the presence of the check. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/mailflow-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-MF-05 — `EnableSafeBrowsing` meta-data is declared outside `<application>` and is therefore inert

| Finding `D-MF-05` | **Low** · CVSS 3.1 3.1 · component **MailFlow** |
|---|---|
| **The issue** | `EnableSafeBrowsing` meta-data is declared outside `<application>` and is therefore inert |
| **Suggested fix** | Move the `EnableSafeBrowsing` `<meta-data>` element inside `<application>`. |
| **What was tested** | The **MailFlow** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/mailflow-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed exactly — the `<meta-data>` sits at manifest level, **before `<application>` opens at `:23`**, so Android does not honour it.]* |
| **How to resolve** | Move the element inside `<application>`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/mailflow-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-SP-01 — The Graph service root is taken verbatim from HPAM-supplied remote config, and `AuthInterceptor` attaches the user's Entra bearer token to every request on that client with no host allow-list

| Finding `D-SP-01` | **High** · CVSS 3.1 7.5 `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` · component **CypherSharePoint** |
|---|---|
| **The issue** | The Graph service root is taken verbatim from HPAM-supplied remote config, and `AuthInterceptor` attaches the user's Entra bearer token to **every** request on that client with no host allow-list |
| **Suggested fix** | Pin `graphApi` to a compile-time allow-list of Microsoft national-cloud hosts, and short-circuit `AuthInterceptor` so the Authorization header is attached only for hosts on that list. |
| **What was tested** | The **CypherSharePoint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/cyphersharepoint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[CONFIRMED EXACTLY 2026-09-09 — the strongest row in seat C's partition.** `AuthInterceptor.kt` read in full (22 lines): it attaches `Bearer` to every request on the shared client with **no inspection of `originalRequest.url`** — no host, scheme or domain test. `GraphProvider.kt:44-48` takes `cloudConfig` across the HPAM IPC boundary and `:61` sets `serviceRoot` from it with **no validation in between**. **Negative claim re-run:** any `startsWith\|endsWith\|contains\|allow\|valid\|whitelist\|check\|require\|host` test on `graphApi`/`oAuthAuthority` across both app trees returns **zero hits**; positive control returns the cited line, so pattern and scope are live. *(Sensitivity recorded rather than adopted: `PR:N` is arguable and gives 7.8 — **High either way**, so the filed `PR:L` stands.)* **`[GAP]`:** the exploit precondition is control of HPAM's `cloudconfig` channel, and whether that channel is signature-protected on HPAM's side lives in another component.] |
| **How to resolve** | Pin `graphApi` to a compile-time allow-list of Microsoft national-cloud hosts (UniversalPrint does exactly this for four clouds in `remoteconfig/PrintCloudConfig.kt:19,29,39,49`), reject anything outside it, and short-circuit `AuthInterceptor` so the Authorization header is attached only for hosts on that list. **Not checked:** the `usermanagement`/`cloudconfig` AAR internals (binary, out of component). `[GAP]` *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cyphersharepoint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-SP-02 — Microsoft Graph SDK logger is wired at `LoggerLevel.DEBUG` into the live Graph client, and the whole cloud config is logged

| Finding `D-SP-02` | **Low** · CVSS 3.1 **3.3** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` · component **CypherSharePoint** |
|---|---|
| **The issue** | Microsoft Graph SDK logger is wired at `LoggerLevel.DEBUG` into the live Graph client, and the whole cloud config is logged |
| **Suggested fix** | Do not attach a DEBUG Graph logger in shipped builds, remove the cloud-config log line, and strip `Log.*` in release. |
| **What was tested** | The **CypherSharePoint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/cyphersharepoint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[PARTLY REFUTED 2026-09-09 — Medium 5.5 to Low 3.3.** The logging is confirmed at source (`GraphProvider.kt:50,52-53,58`). **`C:H` is not established:** it rests on the vendored Graph SDK logging the `Authorization` header, and the SDK ships as a binary `.aar`. The verifier extracted it to scratch and read `DefaultHttpProvider.class`'s constant pool — the header-logging *mechanism* demonstrably exists (`shouldLogVerbosely`, `requestHeaders`, `authenticateRequest` in one class) but whether the bearer reaches logcat turns on call ordering, which needs a decompile. **Scored on what is established: config disclosure to a logcat-privileged caller.** **GATE: if the SDK is shown to log the `Authorization` header at DEBUG, `C:H` restores and the row returns to Medium 5.5.** One decompilation, unblocked by the tenant question.] |
| **How to resolve** | Do not attach a DEBUG logger in shipped builds (mirror MailFlow's commented-out call, or gate on `BuildConfig.DEBUG`); remove `Log.d(TAG, "CloudConfig: …")`; enable R8 and strip `Log.*` via ProGuard rules. **Add CypherSharePoint to F-19's affected-components list.** *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cyphersharepoint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-SP-03 — The OnGuard native locker in the SharePoint APK ships OAuth/vault credential sets for six cloud providers, only one of which the app uses — and the gate that guarded them is disabled

| Finding `D-SP-03` | **Medium** · CVSS 3.1 6.2 · component **CypherSharePoint** |
|---|---|
| **The issue** | The OnGuard native locker in the SharePoint APK ships OAuth/vault credential sets for **six** cloud providers, only one of which the app uses — and the gate that guarded them is disabled |
| **Suggested fix** | Delete the five unused providers' credential sets and rebuild, restore the gate call at `auth.cpp:11` with F-13's signature check, and rotate the foreign providers' identifiers. |
| **What was tested** | The **CypherSharePoint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/cyphersharepoint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed exactly — same disabled `auth.cpp` gate, all `locker.cpp` call sites live.]* |
| **How to resolve** | (1) Delete the five unused provider rows from `secrets.h` and rebuild — a SharePoint app has no business shipping Box/Dropbox/Google Drive credentials. (2) Restore the call at `auth.cpp:11` **and** implement the F-13 signature check. (3) Verify by asserting `isApplicationAuthorized` returns `false` for an unauthorised caller, not by inspecting the presence of the check. (4) Treat the five foreign providers' client identifiers as disclosed and rotate/deregister as their terms require. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cyphersharepoint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-SP-04 — The custom permission that guards the HPAM token IPC is declared with no `protectionLevel` (defaults to `normal`), and the app declares it without requesting it

| Finding `D-SP-04` | **Low** · CVSS 3.1 **3.6** `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:N` · component **CypherSharePoint** |
|---|---|
| **The issue** | The custom permission that guards the HPAM token IPC is declared with no `protectionLevel` (defaults to `normal`), and the app declares it without requesting it |
| **Suggested fix** | Declare the permission in HPAM only, at `android:protectionLevel="signature"`; consumer apps should carry `<uses-permission>` alone. |
| **What was tested** | The **CypherSharePoint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/cyphersharepoint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: `AC:L` to `AC:H` — the downgrade bites only if this app's `normal` declaration wins, which depends on **install order** relative to HPAM. 3.3 to 3.6, **Low confirmed**; this refutes round 1's proposed Low to Medium move.]* **[CROSS-SEAT TENSION, unresolved — §2.3.7 open item 4.** Seat A's out-of-partition note argues `PR:N` rather than `PR:L`, because an Android `normal` permission is auto-granted at install. **On `PR:N` this row computes 4.0 — a Medium** (`AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`). Seat C owns the partition, re-derived at source and kept `PR:L`; seat A explicitly disclaimed its own note as out-of-partition. **Not applied. One metric decides the band and no seat was positioned to settle it.**] |
| **How to resolve** | Declare the permission in **HPAM only**, with `android:protectionLevel="signature"`. Consumer apps should carry `<uses-permission>` alone. Verify HPAM's declaration. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cyphersharepoint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-SP-05 — Outbound e-mail falls back to the network host name as the `From` address

| Finding `D-SP-05` | **Info** · no CVSS score recorded · component **CypherSharePoint** |
|---|---|
| **The issue** | Outbound e-mail falls back to **the device's configured default `From` address, provenance unverified** — |
| **Suggested fix** | Set the `From` address from configuration and never fall back to the device's own default; the provenance of that default is not established by this component. |
| **What was tested** | The **CypherSharePoint** component, as provided in the source snapshot. The claim under test: *Outbound e-mail falls back to the network host name as the `From` address*. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/cyphersharepoint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[wording corrected 2026-09-09: the fallback itself is confirmed at `ScanDescriptionAppFragment.java:305-317`, but the characterisation "the network host name" is **not established** — `Email.getDefaults` is HP Workpath SDK, binary and not in this tree. Informational band correct; no score warranted.]* |
| **How to resolve** | Set the outbound `From` address from application configuration and validate it; remove the fallback to the device's configured default. If a device-supplied default is genuinely required, establish and document its provenance — this component cannot, which is why the row is Informational rather than scored. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D1 — Mutable shared container tag: any repository writer can overwrite the exact image all four production Keycloak instances run

| Finding `I-D1` | **Critical** · CVSS 3.1 **9.1** `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` · component **infra_hpam** |
|---|---|
| **The issue** | Mutable shared container tag: any repository writer can overwrite the exact image all four production Keycloak instances run |
| **Suggested fix** | Pin the image by digest, enable ACR tag immutability, restrict the push workflow to protected refs behind a reviewed environment, and sign images and verify at deploy. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[HIGH 8.0 to CRITICAL 9.1, 2026-09-09.** Vector holds; the arithmetic did not, and the blast-radius claim is provable at source in a way the reviewer did not use. The finding cites `keycloak.V26/main.tf:116` as proof the dev registry is production's source; **that line resolves at apply time and does not establish it.** What does: every Keycloak secret is fetched from App Configuration **with an environment label** (`local.env_name`), and the **three `ContainerRegistry:*` keys are the only ones fetched unlabelled** — so all four production regions, dev, dev-staging, demo and the pdf-api stack resolve to **one registry, by construction in the code**. The labelled keys are the internal positive control. **NOT TESTED:** the *value* of `ContainerRegistry:Url` resolves at apply time and needs a live tenant read, **which is held**; if the strings turn out to differ, `S:C` and the impact metrics must be revisited.] |
| **How to resolve** | (1) Pin by digest: `docker_image_name = "keycloak@sha256:<digest>"`, changed via PR. (2) Enable ACR **tag immutability** (locked repositories) on `keycloak`, and split dev and prod registries or at least dev and prod repositories. (3) Restrict `push_keycloak` to protected refs and require a GitHub Environment with reviewers; `github.ref != 'refs/heads/main'` is not an authorisation control. (4) Bind the variable before the shell: `env: { KC_VERSION: "${{ vars.KEYCLOAK_VERSION }}" }` then use `"$KC_VERSION"`, and validate it against `^v[0-9]+\.[0-9]+$`. (5) Drop `--all-tags`; push the explicit tag. (6) Sign images (cosign / ACR content trust) and verify at deploy. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D2 — Terraform is the mechanism that keeps regenerating the F-16 master credentials, and the App Services cannot stop using them

| Finding `I-D2` | **Critical** · CVSS 3.1 **9.9** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` · component **infra_hpam** |
|---|---|
| **The issue** | Terraform is the mechanism that keeps regenerating the F-16 master credentials, and the App Services cannot stop using them |
| **Suggested fix** | Move App Configuration access to a managed identity so no read key exists as an application setting, delete the plaintext injection at `cc-api/main.tf:96`, and rotate every credential currently written into state. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[HIGH 8.6 to CRITICAL 9.9, 2026-09-09.** The filed `PR:N` **is** wrong — both copies of the state are behind authentication — but correcting it to `PR:L` does not rescue the band: **the filed 8.6 was not reachable from any defensible vector** (`PR:N` gives 10.0, `PR:L` 9.9, even `PR:H` 9.0; only dropping `S:C`, which the source supports keeping, reaches High). Confirmed from the state file **by attribute name only, no values read**: `primary_write_key` present and non-empty, `sensitive_attributes` `[]`, `local_auth_enabled` `true`, `purge_protection_enabled` `false`. **This is the mirror image of `H-D1`** — there, re-deriving the vector moved a row *down* out of Critical; here it confirms one *into* it.] |
| **How to resolve** | The order matters, because rotation without the first step regenerates the problem. (1) Give the App Services a managed identity with `App Configuration Data Reader` and remove the read key from application settings, so `cc-api/main.tf:96` has nothing to inject. (2) Delete the plaintext `app_settings` injection itself. (3) Rotate the App Configuration master keys, the Keycloak database password, the bootstrap administrator password and the ACR password, all of which are in state. (4) Move Terraform state to a backend with customer-managed keys and restricted access, and purge the committed `terraform.tfstate.backup`. **This finding is the mechanism behind F-16, so F-16's remediation is incomplete until this one is applied — see §3.3.5.** |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D10 — No network isolation is deployed anywhere in the topology; the only boundary code in the repository is the commented-out `modules/vnet`

| Finding `I-D10` | **Medium** · CVSS 3.1 **n/a — posture finding** · component **infra_hpam** |
|---|---|
| **The issue** | No network isolation is deployed anywhere in the topology; the only boundary code in the repository is the commented-out `modules/vnet` |
| **Suggested fix** | Finish and enable `modules/vnet` — including the missing NSG associations, without which the rules do nothing — VNet-integrate the App Services, and put private endpoints on App Configuration and Postgres. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: **vector WITHDRAWN, band unchanged.** This is an architectural baseline that is not met, not a vulnerability: `PR:N` + `C:L/I:L/A:L` computes **7.3 High** purely because no barrier metric is present to divide it down. An unauthenticated attacker gains nothing from "no VNet is deployed" on its own. The mechanical band-crosser table's "to High 7.3" is **REFUTED**. The fix is not a better number; it is no number, plus a stated band and reason.]* |
| **How to resolve** | Finish and enable `modules/vnet`: fix the two defects noted in §0a (scope `destination_address_prefix` to the backend subnet; justify or remove the port-80 rule), add the missing `azurerm_subnet_network_security_group_association` resources without which the NSGs do nothing, VNet-integrate the App Services, put private endpoints on App Configuration and Postgres, and front the public path with Application Gateway + WAF. Then close PE-56/PE-95 against evidence rather than intent. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D11 — The app-registration alert container bakes a tenant-wide service-principal credential into an image layer and passes it on the `az` command line

| Finding `I-D11` | **Medium** · CVSS 3.1 6.5 `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` · component **infra_hpam** |
|---|---|
| **The issue** | The app-registration alert container bakes a tenant-wide service-principal credential into an image layer and passes it on the `az` command line |
| **Suggested fix** | Pass the service-principal credential at run time rather than baking it into an image layer, and replace it with a managed or workload identity. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: `I:L` to `I:N` — the script only reads (`az ad app list`), as the finding's own text says. **The re-derived vector reproduces the filed number 6.5 exactly.** "to High 7.3" REFUTED.]* |
| **How to resolve** | Take the credential out of the image: pass secrets at **run** time (`--env-file`, or a container-app secret reference), never `ARG`/`ENV` at build. Use a managed identity or workload identity federation instead of a client secret. Use `az login --service-principal --password @/run/secrets/...` or `AZURE_CLIENT_SECRET` from the environment rather than the command line. Quote all variable expansions. Scope the principal to `Application.Read.All` and nothing more, and confirm that is genuinely required rather than a convenience. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D3 — Keycloak trusts a client-supplied `Forwarded` header: the CLI proxy-header setting overrides the app setting, and Azure App Service does not sanitise that header

| Finding `I-D3` | **Medium** · CVSS 3.1 5.3 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N` · component **infra_hpam** |
|---|---|
| **The issue** | Keycloak trusts a client-supplied `Forwarded` header: the CLI proxy-header setting overrides the app setting, and Azure App Service does not sanitise that header |
| **Suggested fix** | Set `--proxy-headers=xforwarded` so the image and the infrastructure agree on one owner of the setting, and verify the front end overwrites rather than appends `X-Forwarded-For`. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed at source, vector and number both already correct. No change.]* |
| **How to resolve** | Set `--proxy-headers=xforwarded` in the `ENTRYPOINT` so image and infrastructure agree (or drop it from the `ENTRYPOINT` entirely and let `KC_PROXY_HEADERS` govern — one owner, not two). Verify the front end overwrites rather than appends `X-Forwarded-For`. Re-check that realm brute-force detection is enabled once client IPs are correct. Reconsider `--hostname-strict=false`: `KC_HOSTNAME` is pinned at `main.tf:146` so the frontend URL is fixed, but strict hostname is a cheap defence-in-depth control to give up by default. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D4 — The Keycloak database is in public-access mode with its firewall managed by hand, outside Terraform, per the project's own runbook

| Finding `I-D4` | **Medium** · CVSS 3.1 **5.9** `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:N` · component **infra_hpam** |
|---|---|
| **The issue** | The Keycloak database is in public-access mode with its firewall managed by hand, outside Terraform, per the project's own runbook |
| **Suggested fix** | Take the Postgres server off public access with a delegated subnet and a private DNS zone, and bring any firewall rules that must remain into Terraform so they are reviewable. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: `PR:N` to `PR:H` — the finding's own impact claim presupposes the admin credential; a network-exposed Postgres without credentials yields a login prompt. "to High 7.4" **REFUTED**; the reviewer's band was right. The verifier deliberately did **not** chain `I-D2`'s state exposure to supply the credential — that is the double-count that put `H-D1` in the wrong band.]* |
| **How to resolve** | Bring the boundary into code: `public_network_access_enabled = false` with `delegated_subnet_id` + `private_dns_zone_id`, and VNet-integrate the App Services (this is what `modules/vnet` was presumably for — see I-D10). If public access must remain for now, declare explicit `azurerm_postgresql_flexible_server_firewall_rule` resources in Terraform so the rule set is reviewable and drift-detectable, and delete the manual step from the runbook. Enable Microsoft Entra authentication on the flexible server so the admin password stops being the only gate. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D5 — All three App Service modules leave `ftps_state` at the `AllAllowed` default, exposing a plaintext FTP publishing endpoint on the identity provider and the HPAM API

| Finding `I-D5` | **Medium** · CVSS 3.1 5.9 `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:N` · component **infra_hpam** |
|---|---|
| **The issue** | All three App Service modules leave `ftps_state` at the `AllAllowed` default, exposing a plaintext FTP publishing endpoint on the identity provider and the HPAM API |
| **Suggested fix** | Set `ftps_state = "Disabled"` in all three App Service `site_config` blocks, and disable basic publishing credentials. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: same `PR:N` to `PR:H` correction (the finding's own sentence says "anyone who **obtains the publishing profile**" — that is a credential). **The re-derived vector reproduces the filed number 5.9 exactly.** "to High 7.4" REFUTED.]* |
| **How to resolve** | Add `ftps_state = "Disabled"` to all three `site_config` blocks (or `"FtpsOnly"` if a publishing path is genuinely required), and consider `scm_use_main_ip_restriction` / `basic_auth_enabled = false` to disable basic publishing credentials outright. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D6 — Production has no security telemetry: zero diagnostic settings, no authentication-failure alerting, and detailed error messages plus failed-request tracing enabled in all four prod regions

| Finding `I-D6` | **Medium** · CVSS 3.1 4.3 `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` · component **infra_hpam** |
|---|---|
| **The issue** | Production has no security telemetry: zero diagnostic settings, no authentication-failure alerting, and detailed error messages plus failed-request tracing enabled in all four prod regions |
| **Suggested fix** | Add diagnostic settings shipping to Log Analytics on every App Service and Postgres server, alert on 401/403 rates and Keycloak lockouts, and turn detailed errors and failed-request tracing off in production. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed at source, vector and number both already correct. No change.]* |
| **How to resolve** | Add `azurerm_monitor_diagnostic_setting` on each App Service and the Postgres servers, shipping to Log Analytics with a defined retention. Add `Http401`/`Http403` rate alerts and a Keycloak brute-force/lockout event alert to `alerts.tf` alongside the existing 5xx rules. Set `detailed_error_messages = false` and `failed_request_tracing = false` for `var.environment == "Production"`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D7 — The cryptographic `SALT` for the HPAM API is generated by `random_string`, not `random_password`: it is non-sensitive, printed in plan output, and stored in state

| Finding `I-D7` | **Medium** · CVSS 3.1 5.3 `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N` · component **infra_hpam** |
|---|---|
| **The issue** | The cryptographic `SALT` for the HPAM API is generated by `random_string`, not `random_password`: it is non-sensitive, printed in plan output, and stored in state |
| **Suggested fix** | Generate the salt with `random_password` at minimum, and better inside the application at first run with the value held in Key Vault; rotate the current salts and treat them as disclosed. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: `PR:N` to `PR:L` (reading plan output or state requires credentials). **The re-derived vector reproduces the filed number 5.3 exactly.**]* |
| **How to resolve** | Switch to `random_password` (sensitive, redacted) at minimum. Better: generate the salt inside the application at first run and store it in Key Vault, so it never enters Terraform state or plan output; better still, follow F-05's remediation and stop deriving a long-lived secret from a public identifier at all. Rotate the current salts and treat them as disclosed. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D9 — The estate-wide gitleaks rollout is inert: 25 repositories now run a secret-scanning workflow, and every one of them pins a version of `actions/checkout` that does not exist

| Finding `I-D9` | **Medium** · CVSS 3.1 **n/a — posture finding** · component **infra_hpam** |
|---|---|
| **The issue** | The estate-wide gitleaks rollout is inert: 25 repositories now run a secret-scanning workflow, and every one of them pins a version of `actions/checkout` that does not exist |
| **Suggested fix** | Change `actions/checkout@v7` to a version that exists, pinned to a commit SHA, then read the Actions run history and make the gitleaks job a required status check. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed exactly at source (`gitleaks.yml:18` pins `actions/checkout@v7`, which does not exist, so the job fails at checkout). **Vector WITHDRAWN, band unchanged** — this is a control that does not fire, not a vulnerability; its filed vector computes 6.5 and would have promoted the row on nothing.]* **[SEE §2.3.7 open item 2 — the estate-wide reach of this defect is UNDERSTATED in this register.]** |
| **How to resolve** | Change `actions/checkout@v7` to `actions/checkout@v5` (pinned to a commit SHA, per F-21's own remediation #3) and verify `gitleaks/gitleaks-action`'s current major in all 25 files. Then **check the Actions run history**: if the workflow has never completed successfully in any repository, that is the confirmation, and it also means the entire history has never been scanned — so the first successful run should be treated as a discovery exercise, not a regression gate. Make the gitleaks job a required status check so a failure blocks merge rather than decorating it. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### I-D8 — Dev, staging and demo telemetry is hardwired into the production Log Analytics workspace

| Finding `I-D8` | **Medium** · CVSS 3.1 **5.4** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` · component **infra_hpam** |
|---|---|
| **The issue** | Dev, staging and demo telemetry is hardwired into the production Log Analytics workspace |
| **Suggested fix** | Provision a Log Analytics workspace per environment and reference it by resource rather than by a hand-built resource-ID string. |
| **What was tested** | The **infra_hpam** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/infra-hpam-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[LOW 3.5 to MEDIUM 5.4, 2026-09-09.** Vector holds; arithmetic only. `cc-api/main.tf:44-50` — `workspace_id` is a **hardcoded string literal** naming `keycloak-logworkspace-prod` in rg `datasec-platfrom`, and the module is instantiated for dev, dev-staging and demo as well as all four production regions. **The one Medium/Low crosser in this partition that is real.**] |
| **How to resolve** | Make `workspace_id` a module variable and provision a workspace per environment; at minimum, a separate non-production workspace. Reference it by resource, not by hand-built resource ID string. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/infra-hpam-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-1 — The licensing decision is forgeable without the root CA key: the tenant signing key ships inside every licence, wrapped to a key committed in cleartext, and the validation token carries no tenant, issuer, audience or expiry binding

| Finding `NEW-1` | **Critical** · CVSS 3.1 **10.0** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` · component **License-Services** |
|---|---|
| **The issue** | The licensing *decision* is forgeable without the root CA key: the tenant signing key ships inside every licence, wrapped to a key committed in cleartext, and the validation token carries no tenant, issuer, audience or expiry binding |
| **Suggested fix** | Stop shipping the tenant signing key inside the artefact it signs for, bind the validation token with `iss`, `aud`, `tenantId`, `exp`, `nbf` and a server-consumed `jti`, and put the tenant identity in the certificate. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[CONFIRMED AT CRITICAL 2026-09-09, and the load-bearing step is now EXECUTED rather than argued.** The committed API key, from *either* repository, successfully RSA-OAEP-unwraps the content-encryption key of a real committed licence (32-byte CEK, exactly what A256GCM requires); the **negative control** — same ciphertext, same pipeline, committed **root CA** key — **fails**, as a non-recipient key must. *(The recovered key was never written to disk and no value is recorded; only its length.)* **Vector moved and the band did not:** `C:L` to `C:H` (what the attacker obtains is every tenant and device private key ever issued, recoverable offline) and `A:H` to `A:N` (`A:H` rested wholly on `F-03` as an aggravator; forging `valid:true` denies nothing). **Round 1's "9.3 base / 10.0 only with the F-03 aggravator" is SUPERSEDED — the base reaches 10.0 on its own and the aggravator dependency is removed.** Two further measurements: the licence that unwrapped **expired 2025-09-04 and unwrapped anyway** — nothing on the attacker's path consults `exp`, so the capability is not bounded by holding a current licence; and **7 committed artefacts share one API/TLS/JWE public key and 7 share one root CA public key across both repositories** — the two "independently deployed" products share the root CA itself. **One honest caveat the register should carry: `AV:N` and `AC:L` in one vector do not describe one attacker** — `AV:N` belongs to the on-path attacker (`AC:H` by CVSS 3.1 §2.1.2) and `AC:L` to the licence holder against their own fleet (`AV:L`/`AV:A`). Scored coherently **both** scenarios are Critical (9.0 and 10.0), so the band is safe, but the row should record which scenario the vector describes. **`[GAP]` still open: the HPAM client's verification code is not in this repository — closing it needs source access, not a live pass, and it can start now.**] |
| **How to resolve** | **Effort: L — this is a protocol change, not a config change.** 1. **Stop shipping the signing key inside the artefact it signs for.** The tenant private key must never leave the portal. Generate it server-side (HSM/Key Vault) at first upload, or have the portal sign with a *service* key and let the licence bind only the tenant's *public* identity. 2. **Bind the assertion.** Add `iss`, `aud`, `tenantId`, `exp` (the documented 5 minutes), `nbf`, `iat` and a server-consumed `jti` to the validation token (`LicenseTokenUtils.cs:77-82`). Use the `JwtPayload(issuer, audience, claims, notBefore, expires, issuedAt)` overload. 3. **Put the tenant identity in the certificate**: issue tenant certs with the tenant GUID in a SAN/OID, `basicConstraints CA:FALSE`, `keyUsage digitalSignature`, and an EKU — then require the client to match the cert's tenant to the tenant it asked about, not merely to chain to the root. 4. **Rotate all three committed keys** (root, API, and the spare in NEW-8) and treat every licence ever issued as compromised. **Rotating only the root does not close this.** 5. Move key custody to Azure Key Vault / an HSM with an audited signing service; remove `EmbeddedResource` key inclusion (`License.Portal.csproj:29`, `License.Generator.csproj:18`). **Residual risk after remediation:** Low. Remaining exposure is compromise of the server-side signing service and the (out-of-repo) client's willingness to enforce the new claims — that client behaviour must be verified separately. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-2 — Loading the Tenants page permanently deletes the licence record of every tenant whose licence fails validation, including every expired licence — and rotating the root CA (the F-11 remediation) would wipe the entire `TenantLicense` table on the next page view

| Finding `NEW-2` | **Medium** · CVSS 3.1 **6.5** `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:H/A:H` · component **License-Services** |
|---|---|
| **The issue** | Loading the Tenants page permanently deletes the licence record of every tenant whose licence fails validation, including every expired licence — and rotating the root CA (the F-11 remediation) would wipe the entire `TenantLicense` table on the next page view |
| **Suggested fix** | Remove the delete from a read path entirely — render an expired or invalid licence as a state — and add a pre-flight assertion to the root-rotation runbook before F-11 is executed. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[HIGH to MEDIUM 6.5, 2026-09-09 — A SCORING CORRECTION, NOT A RETRACTION, AND THE OPERATIONAL WARNING MATTERS MORE THAN THE BAND.** The defect is confirmed line for line (`TenantLicenseService.cs:48-55` — a silent permanent delete on a rendering path; `ValidateLifetime = true`, so an **expired** licence takes it). Every metric was tested for a route back to High and there is none: **all four handlers that reach it are guarded by `IsHomeDatasecUser()`** (`:40, :58, :76, :93`, enumerated not sampled), so `PR:H` cannot be lowered, and `I:H`/`A:H` are already at maximum. **CVSS IS THE WRONG INSTRUMENT FOR THIS ROW AND MEDIUM MUST NOT REORDER IT IN A REMEDIATION QUEUE.** The dominant scenario has no attacker in it: an expiry passes, an admin opens the page, the record is destroyed. The second is worse and also has no attacker: **executing `F-11`'s remediation (rotate the root CA) makes every stored licence fail validation, and the next Tenants page load deletes the entire table.** CVSS prices both at zero. **Its correct priority is "blocker on the `F-11` root-rotation runbook" — a sequencing fact, not a severity fact.** *(Creditably, `TenantLicenseBackfillHostedService` **skips** rather than deletes — the correct pattern, in the same codebase, which makes the read path's choice a decision rather than an oversight.)*] |
| **How to resolve** | **Effort: S.** Remove the delete from a read path entirely. Render expired/invalid licences as a state (`Expired`, `Invalid signature`) instead of deleting them; if cleanup is genuinely wanted, make it an explicit, confirmed, audited admin action with a soft-delete/archive table. Add a pre-flight assertion to the root-rotation runbook. Distinguish "expired" (`ValidateLifetime` failure) from "untrusted" (signature failure) — `LicenseValidationResult.Reason` already carries enough to do so at `LicenseValidator.cs:30`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-3 — Anonymous, internet-facing customer enumeration: `/api/validate` discloses which Azure AD tenants are HP Authentication Suite licensees

| Finding `NEW-3` | **Medium** · CVSS 3.1 5.3 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` · component **License-Services** |
|---|---|
| **The issue** | Anonymous, internet-facing customer enumeration: `/api/validate` discloses which Azure AD tenants are HP Authentication Suite licensees |
| **Suggested fix** | Return one identical opaque response for every failure mode, rate-limit `/api/validate` per source, and put the device API behind mTLS or a per-tenant credential. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed outright — vector and score both exact. A correctly scored row.]* |
| **How to resolve** | **Effort: S.** return an identical opaque response for "no such tenant", "invalid licence" and "device not licensed" — the device does not need to know which. Remove `request.TenantId` and `validationResult.Reason` from response bodies (`:87,102`). Rate-limit `/api/validate` per source. Put the device API behind mTLS or a per-tenant credential (this also closes the F-10 Portal path). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-4 — Every authenticated user of every Azure AD tenant on earth is a full licensing administrator for their own tenant: no role, group or app-role check exists anywhere in the codebase

| Finding `NEW-4` | **Medium** · CVSS 3.1 **6.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L` · component **License-Services** |
|---|---|
| **The issue** | Every authenticated user of every Azure AD tenant on earth is a full licensing administrator for their own tenant: no role, group or app-role check exists anywhere in the codebase |
| **Suggested fix** | Define Entra app roles, require them with `[Authorize(Policy=…)]` on every mutating handler, and restrict `AzureAd.TenantId` from `common` to an explicit allow-list of customer tenants. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed; the filed vector reproduces 6.3, not 6.7. The reviewer's confirmed-absence control was re-run and **fires**: role/policy vocabulary over all `*.cs`/`*.cshtml` returns **zero hits**; positive control `[Authorize` returns **exactly one hit at the cited line**. The verifier considered `I:L` to `I:H` (which would have produced 7.1 and a Medium-to-High move) and **rejected it** — the actor is confined to their own tenant, so relative to a multi-tenant portal the loss is partial. Recorded so the judgement is visible rather than silent.]* |
| **How to resolve** | **Effort: M.** define app roles in the Entra app registration (e.g. `Licensing.Admin`, `Licensing.Reader`), require them with `[Authorize(Policy=...)]` on every mutating handler, and replace the default that treats any authenticated caller as a permitted one. Restrict `AzureAd.TenantId` from `common` to an explicit allow-list of customer tenant GUIDs (or gate at first sign-in against the `TenantLicense` table). Make device-registration deletion an audited, rate-limited action. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-5 — Cross-tenant super-admin is granted by an unanchored substring regex over the user's UPN

| Finding `NEW-5` | **High** · CVSS 3.1 **7.1** `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` · component **License-Services** |
|---|---|
| **The issue** | Cross-tenant super-admin is granted by an unanchored substring regex over the user's UPN |
| **Suggested fix** | Replace the unanchored UPN regex with an Entra app-role or security-group claim check; if a domain test must remain as defence in depth, anchor it and exclude `#EXT#` principals. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[MEDIUM to HIGH 7.1, 2026-09-09. Every metric of the filed vector is supportable at source: the vector was right and the number was not.** `RegexExtnesions.cs:7` — `[GeneratedRegex(@"@[^@\s]*datasec[^@\s]*\.com")]` with **no `^`, no `$`**, called via `IsMatch` at `UserService.cs:25`. `PR:L` **and not lower** — `:23` requires `HomeTenantId == UsersTenantId` first. `AC:H` **and correctly so** — success needs a `*datasec*.com` verified domain or an `#EXT#` guest UPN shape to exist in the home tenant, a condition outside the attacker's control; that metric is what keeps the row out of the 8s and it is honestly set. `C:H`/`I:H` enumerated: the predicate gates **exporting every customer's licence data** (`Tenants.cshtml.cs:74-89`) and **bulk-deleting any customer's licence** (`:91-105`). **REVISIT GATE:** if the home tenant is ever confirmed to hold no `*datasec*.com` domain beyond the legitimate one and no `#EXT#` guests, exploitability drops and **this row returns to Medium**. **That is a live tenant check, it is Kam's, and no verifier went near it** — `AC:H` already prices the uncertainty, which is why the up-score is safe to take now. *(Seat A's out-of-partition note read the filed Medium as a reasoned hold pending exactly that check; seat A explicitly disclaimed it, and seat B, which owns the partition, re-derived at source and answered it. Recorded in §2.3.7 open item 5.)*] |
| **How to resolve** | **Effort: S.** replace with an Entra **app role or security-group** claim check (`Licensing.GlobalAdmin`), assigned in the directory and validated from the token. If a domain test must remain as defence in depth, anchor it (`^[^@]+@(datasec\.com\.au\|datasec\.com)$`) and exclude `#EXT#` principals explicitly. Log every home-admin action with the acting UPN. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-8 — The committed private-key inventory is larger than recorded, and the artefacts missing from it are exactly the ones text-pattern scanning cannot see — including a third, distinct, undocumented 4096-bit private key; meanwhile the repository's gitleaks workflow cannot block a deploy

| Finding `NEW-8` | **Medium** · CVSS 3.1 5.9 `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N` · component **License-Services** |
|---|---|
| **The issue** | The committed private-key inventory is larger than recorded, and the artefacts missing from it are exactly the ones text-pattern scanning cannot see — including a **third, distinct, undocumented 4096-bit private key**; meanwhile the repository's gitleaks workflow cannot block a deploy |
| **Suggested fix** | Rotate all three keys, purge them from history and verify the purge with a binary-aware scan, and make the gitleaks job a required status check and a `needs:` dependency of the deploy job. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed and **evidence strengthened**. `image_cache.bin` re-measured independently: gzip magic, then PEM, then **4096-bit RSA**, a third distinct key matching neither the API key nor the root key; both copies byte-identical. **One correction that makes the row stronger:** the gitleaks workflow's checkout is **`actions/checkout@v7`**, not the `@v4` filed — the only `@v7` in the repository, and `actions/checkout` has no v7, **so the job fails at its first step and the scan never runs at all**, a more fundamental reason it cannot gate a deploy than the one filed. Also confirmed: the workflow is named "Build, **Test** and Deploy" and contains **no test step** (target grep exit 1, positive control 20 `name:` hits).]* **[SEE §2.3.7 open item 2.]** |
| **How to resolve** | **Effort: M.** rotate all three keys; purge them from history (BFG/filter-repo) — noting that history purge is insufficient on its own while the sibling repo's committed `.exe` still carries the root key (see the LicenseServer file, NEW-3). Add `*.pem`, `*.key`, `*.bin`, `*.pfx` to `.gitignore` (currently `:247` ignores only `*.pfx`). Make the gitleaks job a **required** status check via branch protection **and** a `needs:` dependency of the deploy job; add `--redact` plus an entropy/binary rule set, or a purpose-built binary-secret scan. Delete `image_cache.bin` and document what it was. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-10 — `Jose.JWT.Decode` is called with no expected algorithm, in the one place the sibling implementation constrains it

| Finding `NEW-10` | **Low** · CVSS 3.1 **3.3** `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:N` · component **License-Services** |
|---|---|
| **The issue** | `Jose.JWT.Decode` is called with no expected algorithm, in the one place the sibling implementation constrains it |
| **Suggested fix** | Pass the expected algorithms to the decode call: `JWT.Decode(metadata.Key, apiKey, JweAlgorithm.RSA_OAEP, JweEncryption.A256GCM)`. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed; 3.1 to 3.3, band unchanged. The reviewer's "not exploitable today" is correct and precisely reasoned.]* |
| **How to resolve** | **Effort: S.** `JWT.Decode(metadata.Key, apiKey, JweAlgorithm.RSA_OAEP, JweEncryption.A256GCM)`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-6 — Security headers never reach unauthenticated or static responses: `SecurityHeadersMiddleware` is registered after the two middlewares that short-circuit

| Finding `NEW-6` | **Medium** · CVSS 3.1 4.7 `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N` · component **License-Services** |
|---|---|
| **The issue** | Security headers never reach unauthenticated or static responses: `SecurityHeadersMiddleware` is registered after the two middlewares that short-circuit |
| **Suggested fix** | Move `SecurityHeadersMiddleware` to immediately after `UseHttpsRedirection()` so it runs before the two middlewares that short-circuit, and drop `'unsafe-eval'` and `'unsafe-inline'` from the policy. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[LOW to MEDIUM, 2026-09-09. The number did not change — the band label was simply wrong.** 4.7 is Medium (boundary 4.0); the register declared Low against its own printed 4.7. The middleware order was read in `Program.cs` and is exact: `:82 UseStaticFiles()` and `:105-106 UseAuthentication/UseAuthorization` both short-circuit **before** `:108 UseMiddleware<SecurityHeadersMiddleware>()`. **A band-label correction, not a re-score: no judgement was changed and the row's content is untouched.**] |
| **How to resolve** | **Effort: S.** move `app.UseMiddleware<SecurityHeadersMiddleware>()` to immediately after `UseHttpsRedirection()` (before `UseStaticFiles`). Remove `'unsafe-eval'`; move inline scripts to files and drop `'unsafe-inline'`; restrict `connect-src` to `'self' https://js.monitor.azure.com` (the `http: ws: wss:` grants permit plaintext exfiltration destinations). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-7 — The tenant-selection session cookie is created with framework defaults (not `Secure`, not `SameSite=Strict`, id never regenerated at sign-in), and the one handler that writes it does not re-check home-admin status

| Finding `NEW-7` | **Low** · CVSS 3.1 3.7 `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N` · component **License-Services** |
|---|---|
| **The issue** | The tenant-selection session cookie is created with framework defaults (not `Secure`, not `SameSite=Strict`, id never regenerated at sign-in), and the one handler that writes it does not re-check home-admin status |
| **Suggested fix** | Configure the session cookie `Secure`, `SameSite=Strict` and `HttpOnly` with an idle timeout, re-issue the session at sign-in and sign-out, and add the home-admin check to `OnPostViewTenant`. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed outright — vector and score both exact. The reviewer's control re-run and it **fires**: `Session.Clear` returns zero hits, positive control `Session.SetString` returns exactly 2 hits at the two cited lines. **A row that argued itself down** (`TenantContextMiddleware.cs:13` only reads the session value when `IsHomeDatasecUser()` is true, so a planted value from a non-home user is ignored) — the opposite of the `H-D1` failure, and it deserves crediting.]* |
| **How to resolve** | **Effort: S.** configure `AddSession(o => { o.Cookie.SecurePolicy = Always; o.Cookie.SameSite = SameSiteMode.Strict; o.Cookie.HttpOnly = true; o.Cookie.IsEssential = true; o.IdleTimeout = TimeSpan.FromMinutes(30); })`; clear and re-issue the session on sign-in and sign-out; add the `IsHomeDatasecUser()` check to `OnPostViewTenant` so the page's five handlers are consistent; and prefer a signed, server-validated tenant selector over raw session state. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-9 — Certificate issuance under the licensing root has no extensions, uses predictable serial numbers in both C# generators, and accepts DN injection from a free-text field

| Finding `NEW-9` | **Low** · CVSS 3.1 **3.9** `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:L/I:L/A:N` · component **License-Services** |
|---|---|
| **The issue** | Certificate issuance under the licensing root has no extensions, uses predictable serial numbers in both C# generators, and accepts DN injection from a free-text field |
| **Suggested fix** | Add basic constraints, key usage, an EKU and a tenant SAN to issued certificates, use a cryptographically random serial in both C# generators, and escape the DN components. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[2026-09-09: `AV:N` to `AV:L`, 4.0 to 3.9, band Low CONFIRMED. This is the `H-D1` result reproduced exactly and it is the strongest argument in the pass for the slow method** — the filed vector produces **4.4, a Medium**, and a mechanical sweep would have surfaced it as a Low-to-Medium crosser. Re-deriving at source moves it back **down** and **vindicates the register's declared band.** The vulnerable operation is certificate minting in `License.Generator`, a desktop WinForms application (`MainForm.cs:233-245`) driven by a Company Name typed into a textbox by an operator who already holds the embedded root key. Nothing about minting is bound to a network stack. **Read this row beside LicenseServer `NEW-9`: same defect class, two sibling generators, and they were scored with different access vectors (`AV:N` here, `AV:L` there). `AV:L` is right in both.** After correction they land at 3.9 (Low) and 4.6 (Medium); the residual gap is entirely `AC:H` vs `AC:L` and reflects a real difference in scope of claim — **stated here rather than left to look like a slip.**] |
| **How to resolve** | **Effort: S.** add `req.CertificateExtensions.Add(new X509BasicConstraintsExtension(false, false, 0, true))`, `new X509KeyUsageExtension(DigitalSignature, true)`, an EKU, and a SAN carrying the tenant GUID; use `RandomNumberGenerator.GetBytes(16)` for the serial in both C# generators to match the Python one; construct the subject from escaped components rather than string interpolation. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/license-services-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-11 — No `ValidAlgorithms` allow-list on any JWT validator

| Finding `NEW-11` | **Info** · no CVSS score recorded · component **License-Services** |
|---|---|
| **The issue** | (Informational) — No `ValidAlgorithms` allow-list on any JWT validator |
| **Suggested fix** | Configure an explicit `ValidAlgorithms` allow-list on every JWT validator, so the guarantee rests on the application's own contract rather than on library defaults. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **No per-row test record was written for this row**, so the section method above is the whole of what can be said about how it was tested. That is stated rather than filled in. |
| **How to resolve** | Set `ValidAlgorithms` explicitly on every `TokenValidationParameters` in the product, so the algorithm guarantee is the application's own contract rather than a library default that a dependency upgrade can change. The sibling implementation already constrains the algorithm in one place; make it uniform. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-12 — Security-through-obscurity is a documented practice here

| Finding `NEW-12` | **Info** · no CVSS score recorded · component **License-Services** |
|---|---|
| **The issue** | (Informational) — Security-through-obscurity is a documented practice here. |
| **Suggested fix** | Replace the documented obscurity practice with a stated control, and remove the claim from the documentation. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed, **and a fourth instance added**: the PEM inside `image_cache.bin` is **indented with leading whitespace**, so a naive `openssl pkey` read of it fails — obfuscation layered on top of the deliberately obscure filename. The verifier found this because their own first pipeline silently returned the SHA-256 of an **empty stream** and they chased the discrepancy instead of reporting a clean bill.]* |
| **How to resolve** | Identify each control that the documentation describes as deriving its strength from obscurity, and either replace it with a stated control that survives disclosure of the design, or record explicitly that no control exists there. Obscurity is not a finding on its own; documenting it as a control is. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-13 — LIKE-wildcard injection in the device serial filter

| Finding `NEW-13` | **Info** · no CVSS score recorded · component **License-Services** |
|---|---|
| **The issue** | (Informational) — LIKE-wildcard injection in the device serial filter. |
| **Suggested fix** | Escape the LIKE wildcards in the device-serial filter, or match on equality. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed **with a narrowing** — `Devices.cshtml.cs:156-159`, the `Like` branch fires **only when the term contains `*`**; otherwise `.Contains()` parameterises safely. Narrower than the row implies; Info is still correct.]* |
| **How to resolve** | Escape `%` and `_` in the device-serial filter before it reaches the LIKE clause, or match on equality. The parameterisation is already correct, so this is a wildcard-handling defect rather than an injection into SQL syntax. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-14 — Documentation asserts controls the code does not implement

| Finding `NEW-14` | **Info** · no CVSS score recorded · component **License-Services** |
|---|---|
| **The issue** | (Informational) — Documentation asserts controls the code does not implement. |
| **Suggested fix** | Reconcile the documentation with the code: implement the controls it asserts, or withdraw the assertions. |
| **What was tested** | The **License-Services** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/license-services-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed — the payload at `LicenseTokenUtils.cs:77-84` carries no `iss`/`aud`/`exp`/`nbf` while the docs instruct the client to check them. **Cross-reference added on both seats' recommendation: this is the documentation half of `NEW-1`. Read the two together.**]* |
| **How to resolve** | Go through the documentation's control assertions one by one against the code, and for each either implement the control or withdraw the assertion. Documentation that asserts controls the code does not implement is the failure mode that produced `04_Keycloak_Retirement_Attestation` and §3.3.2. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D1 — Unsigned, unauthenticated job-manifest import is a supply-chain channel into the printer fleet; `ValidateHpkFile` is a metadata extractor whose name asserts a check it does not perform

| Finding `H-D1` | **High** · CVSS 3.1 **8.6** `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | Unsigned, unauthenticated job-manifest import is a supply-chain channel into the printer fleet; `ValidateHpkFile` is a metadata extractor whose name asserts a check it does not perform. |
| **Suggested fix** | Delete the plaintext manifest fallback at `DeploymentJobForm.cs:1311-1313`, sign the manifest and the hashes of every bundled `.hpk` and verify before deserialisation, and make `ValidateHpkFile` validate or rename it. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[RE-SCORED 2026-09-09 — Critical 9.0 to High 8.6. THIS IS A SCORING CORRECTION, NOT A RETRACTION:** the finding, its full evidence chain and all six remediation steps stand unchanged, and it remains the most serious defect in this component. Verified independently at source: the filed vector asserted `AV:N`, which is not supportable — the job file is chosen by the operator through an `OpenFileDialog` (`DeploymentJobForm.cs:1081,377`; `ImportJobAsync(string sourceFile)` to `ZipFile.OpenRead`), and `HttpClient\|WebClient\|DownloadFile\|FtpWebRequest` returns **zero matches across all of `src/`** — the vulnerable component is not bound to the network stack. The fleet-wide blast radius is real and is already carried by `S:C`, which is retained; using it a second time to justify `AV:N` double-counts it, and that double-count was the whole difference between Critical and High. The filed number 9.0 did not match the filed vector either, which produces 9.6. **`AV` REVISIT GATE:** this re-score rests on static analysis only — no live check was performed. **If any non-local deployment path into this import is ever found, `AV` is re-opened and this row returns to Critical.** Separately, the reviewer’s stated positive control for this finding was **refuted** on re-run and replaced with one that fires; the conclusion (no signature or integrity verification anywhere in `src/`) held under the replacement. Full record: `_Working/2026-09-09_VERIFY96_REPORT.md`, Critical 3. Ruled by Tuesday 2026-09-09 under Kam’s v1.3 delegation.] |
| **How to resolve** | 1. **Delete the plaintext fallback** at `DeploymentJobForm.cs:1311-1313`. A failed decrypt must be a hard, visible error. This is a three-line change and it is the single highest-value fix in the component. 2. **Sign the manifest.** Detached signature or HMAC over the canonical manifest bytes **and** over the SHA-256 of every bundled `.hpk`; verify before deserialisation and refuse on mismatch. Under a per-installation DPAPI-derived key this also fixes F-15's key problem; under an organisational signing key it additionally establishes who authored the job. 3. **Make `ValidateHpkFile` validate, or rename it.** At minimum: verify the APK's v2/v3 signature block and pin the expected signer certificate; verify `META-INF` is present and consistent. A method named `Validate…` that performs no validation is how this defect survived a review — the name asserts the control. 4. **Show the operator what they are about to trust.** On import, display the signer, the uuid/version, and whether this replaces or upgrades a known app; require explicit confirmation for an unknown uuid. 5. Treat configuration and attestation payloads as security-sensitive data: sign them with the manifest, store them encrypted (they are plaintext columns today), and diff them against the current fleet state before push. 6. Establish with HP exactly what `--force` relaxes, and gate it behind a separate, logged authorisation. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpk-deployment-utility-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D2 — Arbitrary file write with fully attacker-controlled content: the manifest's `Hpk.FileName` reaches `Path.Combine` and `File.WriteAllBytesAsync` unsanitised

| Finding `H-D2` | **Low** · CVSS 3.1 **3.3** `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N` · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | Arbitrary file write with fully attacker-controlled content: the manifest's `Hpk.FileName` reaches `Path.Combine` and `File.WriteAllBytesAsync` unsanitised |
| **Suggested fix** | Derive the staging filename from the database row id rather than from the manifest, and assert that the canonicalised path still sits inside the staging folder. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[HIGH 7.8 to LOW 3.3 — TWO BANDS, 2026-09-09. The sink is real and confirmed; the taint chain as filed is wrong, and that is the whole finding.** The filed chain (`JobExportDto` to `DeploymentJobForm.cs:410` to DB to `Worker.cs:307`) **does not reach the database by that route**: `:412` populates an in-memory grid DTO that is never written to `Hpks.FileName`; `JobAppRepository.cs:36` shows the Worker reads `IFNULL(Hpks.FileName,'')` **from the `Hpks` table**, and the only tainted write there is `:1364` `FileName = hpk.Name` — i.e. **`ZipArchiveEntry.Name`, not the manifest JSON field.** Three hard constraints the finding did not account for: **(1) the extension is locked** — only `.hpk` entries are considered and the same value becomes the filename, so `evil.exe` and DLL side-loading are **not reachable** and the finding's stated consequence (persistent code execution via the Startup folder) does not follow; **(2) the content must parse as a valid HPK**; **(3) create-only** — `Worker.cs:308` `File.Exists to return true`, so no existing file can be overwritten. Metrics: `C:H` to `C:N`, `I:H` to `I:L`, `A:H` to `A:N`. **NOT TESTED and pivotal:** whether traversal is reachable at all depends on .NET's `ZipArchiveEntry.Name` separator handling; `dotnet` is not installed on the review machine and fetching it is under the holds. **The verifier scored the branch that FAVOURS the attacker, so the row cannot be understated by that gap — the other branch is Informational.** One offline unit test settles it.] |
| **How to resolve** | Never build a path from external input. Derive the staging filename from the database row id (e.g. `hpks/{HpkId}.hpk`) and keep the manifest's filename as display metadata only. If a name must be used, apply `CleanFilename`, reject any value containing a directory separator, `..`, a drive letter or a UNC prefix, then canonicalise with `Path.GetFullPath` and assert the result still starts with `ResourcesUtils.HpksFolder` — the check, not just the sanitiser. Replace the `File.Exists` shortcut at `:308` with a SHA-256 comparison against the stored blob. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpk-deployment-utility-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D5 — The Worker's unauthenticated control plane is the SQLite database and the `hpks/` staging folder, not the stop-signal

| Finding `H-D5` | **High** · CVSS 3.1 **8.8** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | The Worker's unauthenticated control plane is the SQLite database and the `hpks/` staging folder, not the stop-signal **[7.6 to 8.8, band High, 2026-09-09. The vector was right and the number was wrong — and this is 0.2 below Critical.** Every claim reproduces: unencrypted SQLite with no `Password=`/SQLCipher (`DatabaseProvider.cs:15`); an **unbounded** 5-minute polling loop executing `Pending` tasks with **no operator confirmation anywhere on the path** (`Worker.cs:16-62,89-93`); `HpkExeExists()`/`AdbExeExists()` are `File.Exists` and nothing else — no hash, no signature, no publisher (`ToolsUtils.cs:20,24`); **there is no service account** — the Worker runs as the interactive operator (`WorkerServiceUtils.cs:16-33`); and the release is a **`.7z`, not an installer** (`release.yaml:73-75`), which guarantees a user-writable directory and holds `AC:L`. **`UI:N` is the row's teeth:** unlike `H-D1`, no operator action carries the payload — the Worker polls autonomously. **The best-built row in this component.**] |
| **Suggested fix** | Ship an installer that ACLs the data directory, encrypt the SQLite database under a DPAPI-derived key, hash-match staged files instead of testing existence, and verify the Authenticode signature of the tools before invoking them. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The claim under test: *The Worker's unauthenticated control plane is the SQLite database and the `hpks/` staging folder, not the stop-signal*. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **No per-row test record was written for this row**, so the section method above is the whole of what can be said about how it was tested. That is stated rather than filled in. |
| **How to resolve** | (1) Ship an installer that places the application under a system-protected path and sets an explicit ACL on the data directory; document the requirement if an installer is out of scope. (2) Encrypt the database (SQLCipher / `Microsoft.Data.Sqlite` with an encryption provider) under a DPAPI-derived key — this closes surfaces 1 and 6 together with F-15's at-rest problem. (3) Replace `File.Exists` at `Worker.cs:308` with a SHA-256 match against the stored blob (surface 2). (4) Verify the Authenticode signature of `HPKTool-cli.exe` and `adb.exe` before invoking them, and record the verified publisher in the deployment log (surface 3). (5) Replace both file signals with an authenticated IPC channel — a named pipe with an ACL — or at minimum ACL the signal files (surfaces 4 and 5). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpk-deployment-utility-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D3 — Argument injection with a new external taint source: `--uuid` is interpolated unquoted from the attacker-supplied `hpk.xml`

| Finding `H-D3` | **Medium** · CVSS 3.1 **6.1** `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | Argument injection with a new external taint source: `--uuid` is interpolated unquoted from the attacker-supplied `hpk.xml` |
| **Suggested fix** | Stop building the argument string: pass each value as a discrete `argv` element with `ProcessStartInfo.ArgumentList`, and validate `HpkUuid` against the RFC 4122 pattern. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed; **vector corrected `S:U` to `S:C`** — the injected flags enter a CLI invocation against the printer fleet, and the same reviewer chose `S:C` for `H-D1` and `H-D5` on precisely that reach. Added positive control: `EscapeForCli` is defined once and applied at exactly two sites, **never** to `HpkUuid`, `password`, `ipAddress`, `Username` or `LdbServiceKey`; `RegexUtils.cs` defines IPv4 and datetime patterns and **no uuid pattern**. **GATE, written onto the row: `I:H` rests on the finding's own `[UNVERIFIED]` — which flags `HPKTool-cli.exe` accepts. If `I:H` is ever proven the vector gives 7.7 and this row becomes High.** It is one document lookup from High.]* |
| **How to resolve** | Stop building the argument string. `ProcessStartInfo.ArgumentList` passes each value as a discrete `argv` element and eliminates this entire class without needing `EscapeForCli` at all — it is a mechanical change to `CreateHpkProcess` (`Worker.cs:991-1006`) and the four call sites. Independently, validate `HpkUuid` against the RFC 4122 pattern at `HpkServices.cs:60` and reject anything else, and re-validate IPs in `GetIpAddress` rather than trusting the UI to have done it. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpk-deployment-utility-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D4 — The LDB service key is written to the error log in cleartext

| Finding `H-D4` | **Medium** · CVSS 3.1 **4.7** `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N` · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | The LDB service key is written to the error log in cleartext |
| **Suggested fix** | Log a redacted projection rather than the settings object, give the key a type that cannot be serialised by accident, and rotate the key on any installation whose logs have left the machine. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed; **`AC:L` to `AC:H`, the metric the finding missed is its own.** The log site is **inside a `catch`** — the key reaches disk only when the settings save **fails**, a condition beyond the attacker's control; the reviewer's own prose says "on first save failure" while the vector said `AC:L`. Census: exactly **one** log site in the file takes the settings DTO. Medium either way; both readings are below the recorded 6.2.]* |
| **How to resolve** | Never pass a settings DTO as log metadata. Log a redacted projection (`new { appSettingsDto.Username, HasLdbKey = !string.IsNullOrEmpty(appSettingsDto.LdbServiceKey) }`). Better: give `AppSettingsDto.LdbServiceKey` a type that cannot be serialised by accident (a `SecureString`-like wrapper, or `[JsonIgnore]` plus a custom `ToString`), so this cannot recur at a future call site. Audit the other `LogErrorAsync` metadata arguments on the same principle. Rotate the LDB service key on any installation whose logs have left the machine. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpk-deployment-utility-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D6 — Debug symbols are hidden rather than removed from the release archive, and every push to `main` publishes the binary that carries the F-15 hardcoded AES key

| Finding `H-D6` | **Medium** · CVSS 3.1 **6.5** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | Debug symbols are hidden rather than removed from the release archive, and every push to `main` publishes the binary that carries the F-15 hardcoded AES key |
| **Suggested fix** | Remove the `.pdb` files from the release archive rather than hiding them, publish on tags behind an approval gate, and replace the hardcoded AES key with a DPAPI-derived one. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed; **`AV:L` to `AV:N` — the filed vector contradicted the finding's own central argument.** The finding exists to say the "needs local access to the binary" precondition **is satisfied by the pipeline** (the archive is published as a GitHub Release asset on every push to `main`) and then scored `AV:L`, asserting the very precondition it had just refuted. 5.5 to 6.5, band unchanged. **This row's argument bears directly on June `F-15`'s `AV:L/PR:L` rationale — named, not chased.**]* |
| **How to resolve** | `Remove-Item out\*.pdb -Force` (or `<DebugType>none</DebugType>` for release publishes) — and delete the `attrib +h` target so nobody believes the problem is handled. Publish releases on **tags** with an approval gate, not on every push to `main`. Pin all actions to commit SHAs. Symbols, if wanted, belong in a private symbol server, never in the operator-facing archive. And fix the hardcoded key: once the binary is a public artefact by design, DPAPI-derived keys stop being best practice and become the only tenable option. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpk-deployment-utility-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D7 — The estate-wide gitleaks rollout is inert: this repository's secret-scanning workflow pins a version of `actions/checkout` that does not exist

| Finding `H-D7` | **Medium** · CVSS 3.1 **n/a — control failure** · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | The estate-wide gitleaks rollout is inert: this repository's secret-scanning workflow pins a version of `actions/checkout` that does not exist |
| **Suggested fix** | Change `actions/checkout@v7` to a version that exists and make the gitleaks job a required status check — the same one-string fix as `I-D9`, in a second repository. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: the defect is confirmed exactly (`gitleaks.yml:18` pins `actions/checkout@v7`); **the CVSS is refuted as a category error and the vector is removed, band unchanged.** A secret-scanning workflow that does not run has no attacker, no attack vector and no C/I/A impact on any component. The filed vector computes 6.5 (not the recorded 5.3) and describes a remote unauthenticated exploitation of a workflow file. **A control failure carrying a CVSS base score invites exactly the false precision this round was commissioned to remove.**]* **[SEE §2.3.7 open item 2.]** |
| **How to resolve** | Identical to `I-D9`: change `actions/checkout@v7` to a version that exists, pinned to a commit SHA; verify `gitleaks/gitleaks-action`'s current major; read the Actions run history to confirm the job has never completed; and make the job a required status check so a failure blocks a merge rather than decorating it. **Treat the first successful run as a discovery exercise, not a regression gate** — the repository has never been scanned. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D8 — Silence from `HPKTool-cli.exe` is recorded as a successful deployment

| Finding `H-D8` | **Low** · CVSS 3.1 **n/a — assurance finding** *(computes 2.5)* · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | Silence from `HPKTool-cli.exe` is recorded as a successful deployment |
| **Suggested fix** | Default the empty case to `Failure` rather than `Success`, prefer the exit code and the structured output the code already handles, and record the raw output alongside the derived verdict. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed exactly — `Worker.cs:988-991`, silence + exit 0 = `Success`; `AC:L` to `AC:H` gives **2.5**, and the vector is then **removed on the verifier's recommendation.** `H-D8` has no attacker: it is a **record-integrity defect** — the artefact answering *"was the attestation actually installed on all 400 devices?"* can assert success it never observed. **That is worth more to a defence customer than 2.5 suggests, and a CVSS base score is the wrong instrument for it.**]* |
| **How to resolve** | Default the empty case to `Failure`, not `Success` — absence of evidence is not evidence of success. Prefer the exit code and, if `HPKTool-cli.exe` offers structured output (the code already handles a JSON branch at `:892`), parse that rather than prose. Record the raw stdout/stderr and the exit code alongside the derived verdict so the record is auditable rather than merely asserted. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpk-deployment-utility-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### H-D9 — `SettingsUtils.AppSettings` fires an `async void` load from a property getter, so the first read can silently return empty credentials

| Finding `H-D9` | **Low** · CVSS 3.1 **3.6** `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:L` · component **HPK_Deployment_Utility** |
|---|---|
| **The issue** | `SettingsUtils.AppSettings` fires an `async void` load from a property getter, so the first read can silently return empty credentials |
| **Suggested fix** | Load settings explicitly and awaited at startup, and refuse an attestation install when the username or the service key is empty. |
| **What was tested** | The **HPK_Deployment_Utility** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpk-deployment-utility-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** [2026-09-09: confirmed **Low**, and this REFUTES round 1's proposed Low to Medium move. `AC:L` to `AC:H`: this is a **race** and no attacker controls its timing; the most an attacker can do — with `PR:L` already — is widen the window by contending on the database, which is not a condition they control at will. **Round 1 listed `H-D9` as `3.3 to 4.4, would move Low to Medium` under an explicit warning not to adopt the column. The warning was right.** The reviewer's lower band reflected better judgement than their own vector.] |
| **How to resolve** | Make loading explicit and awaited at startup (`await SettingsUtils.InitialiseAsync()` in both `Program.cs` files) and let the property be a pure accessor over an initialised value. Guard `Worker.cs:812` to refuse an attestation install when `Username` or `LdbServiceKey` is empty, and log the refusal. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpk-deployment-utility-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-1 — The licensing decision is forgeable without the root CA key (mirror of `license-services-main.md` NEW-1, as it manifests here)

| Finding `NEW-1` | **Critical** · CVSS 3.1 **10.0** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` · component **LicenseServer** |
|---|---|
| **The issue** | The licensing decision is forgeable without the root CA key (mirror of `license-services-main.md` NEW-1, as it manifests here) |
| **Suggested fix** | As in the sibling product: stop shipping the signing key inside the licence, bind the assertion with `iss`, `aud`, `tenantId`, `exp`, `nbf` and `jti`, put the tenant GUID in the certificate, and rotate the root, API and spare keys. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[CONFIRMED AT CRITICAL 2026-09-09 — see License-Services `NEW-1` above for the full record, including the executed RSA-OAEP unwrap and its negative control. **This remains the reviewer's own declared mirror: these two rows are ONE distinct defect counted twice by the per-component convention.** Both copies of the key unwrapped the same real licence.]** |
| **How to resolve** | As in the sibling file — stop shipping the signing key inside the artefact it signs for; bind the assertion with `iss`/`aud`/`tenantId`/`exp`/`nbf`/`jti`; put the tenant GUID in the certificate and require the client to match it; rotate root, API **and** the spare key found in the sibling repo, treating every issued licence as compromised. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-2 — One private key serves three different purposes across two independently-deployed products: TLS server key, LicenseServer JWE key, and License.Portal JWE key

| Finding `NEW-2` | **High** · CVSS 3.1 **8.7** `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` · component **LicenseServer** |
|---|---|
| **The issue** | One private key serves three different purposes across two independently-deployed products: TLS server key, LicenseServer JWE key, and License.Portal JWE key |
| **Suggested fix** | Separate the three roles into three keys with three lifecycles, hold the key-transport keys in Key Vault or an HSM, obtain the TLS certificate from a real CA, and rotate all four committed copies. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed; the filed 8.1 is not what the filed vector produces — 8.7 is. All three "hats" measured rather than inferred, and the row **understates itself**: **the root CA is shared between the two products too**, not just the JWE recipient key (7 committed artefacts share one root CA public key across both repositories). That strengthens `S:C` — compromise spans two products' *entire* trust chains.]* |
| **How to resolve** | **Effort: M–L.** separate the three roles into three keys with three lifecycles; move the JWE key-transport keys into Azure Key Vault / an HSM and never persist them in the image or repo; obtain the TLS certificate from a public or enterprise CA rather than the self-signed licensing root; rotate all four committed copies and treat all prior licences as compromised. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-3 — The root CA private key is committed as a compiled binary, so deleting the `.key` file does not remove it from the repository — and the Dockerfile bakes the API key into every published container image

| Finding `NEW-3` | **High** · CVSS 3.1 7.5 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` · component **LicenseServer** |
|---|---|
| **The issue** | The root CA private key is committed as a **compiled binary**, so deleting the `.key` file does not remove it from the repository — and the Dockerfile bakes the API key into every published container image |
| **Suggested fix** | Delete the committed `.exe`, purge both it and the `.key` from history and verify with a binary-aware scan, inject the API key at runtime, and quarantine every published image tag that carries it. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed outright — vector and score both exact. The embedded key was **extracted and identified**: PEM span from `LicenseGenerator.exe` (PE32+, 1,513,290 bytes, exactly one `BEGIN PRIVATE KEY` block), public key `a6b18685…`, **4096-bit, identical to `hpauthsuite_root.key` on disk**; discrimination control confirms it does **not** match the API key. **One wording correction:** the images go to the **dev** registry (`crdevdsec.azurecr.io`, App Service `dev-api-hpam-license`, rg `dev-hpam`) — **this workflow has no production job at all** (all 46 lines read). The conclusion is unaffected (layers are immutable, every tag still carries the key) but a reader would otherwise scope the purge wrongly. **Stated so nobody "fixes" it later: `I:N`/`S:U` are deliberate — this row is scored as a *disclosure*, not as what the key can do, because what it can do is `F-11` and `NEW-1`. That is the correct non-double-counting choice, and it only holds while those rows stand beside it.**]* |
| **How to resolve** | **Effort: M.** delete the committed `.exe`; purge both the `.exe` and the `.key` from history; **verify the purge with a binary-aware scan, not a text scan**. Remove `COPY license_server_ssl/license_server_api.key` from the Dockerfile and inject the key at runtime from Key Vault via a mounted secret or managed identity. Treat every image tag in `crdevdsec.azurecr.io/api-hpam-license` as containing a compromised private key and purge or quarantine the repository. Rotate. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-4 — There is no revocation mechanism of any kind, and the unauthenticated `/upload` makes licence state actively rollback-able: an old, more generous licence can be re-uploaded at any time to restore quota

| Finding `NEW-4` | **High** · CVSS 3.1 7.5 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` · component **LicenseServer** |
|---|---|
| **The issue** | There is no revocation mechanism of any kind, and the unauthenticated `/upload` makes licence state actively **rollback-able**: an old, more generous licence can be re-uploaded at any time to restore quota |
| **Suggested fix** | Reject any upload not strictly newer than the stored licence, add a `jti` and a server-side revocation table consulted on every validate, and authenticate `/upload`. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed outright — vector reproduces exactly. Every cited line read: `:126` `/upload` unauthenticated, `:163-167` unconditional upsert, `:170-171` `RemoveRange` of every serial for the tenant, `:245-247` expiry the only stop. **The reviewer's confirmed-absence control was re-run and it FIRES:** revocation vocabulary (`revoc\|revoke\|crl\|ocsp\|blocklist\|jti\|X509RevocationMode\|X509Chain`) over both trees returns **zero substantive hits**; positive control `maxDevices`, identical instrument and scope returns **60 hits**. The absence is a measurement.]* |
| **How to resolve** | **Effort: M.** add a monotonic licence sequence/`iat` check and reject any upload not strictly newer than the stored licence; introduce a `jti` per licence and a server-side revocation table consulted on every `/api/validate`; stop blanket-deleting serials on upload (cull deterministically, log each removal with attribution); add `exp`/`nbf`/`jti` to the validation token and consume the nonce server-side; authenticate `/upload` (F-10). Longer term, publish a signed revocation list the client checks, or shorten licence lifetimes so expiry *is* the revocation mechanism. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-5 — The licence's own `tenantId` claim is never read: a licence issued for one tenant can be installed as another tenant's licence, and is never re-checked at validate time either

| Finding `NEW-5` | **High** · CVSS 3.1 **8.6** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` · component **LicenseServer** |
|---|---|
| **The issue** | The licence's own `tenantId` claim is never read: a licence issued for one tenant can be installed as another tenant's licence, and is never re-checked at validate time either |
| **Suggested fix** | Read the `tenantId` claim from the validated token and require it to match the submitted tenant, both at upload and again at validate. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed; **vector moved `S:U` to `S:C`**, 7.5 to 8.6, band holds. `Program.cs:219-225` read in full — the claims extracted from the validated token are `maxDevices`, `exp`, `deviceCertPem`, `encKeyBlob`, and **`tenantId` is not among them**; the tenant comes from the caller at `:132`/`:180`. The licence **carries** its own tenant binding (the committed sample proves it) and the server discards it. `S:C` because the exploit installs the attacker's licence under **another customer's** tenant id and wipes that customer's serial ledger — **breaching multi-tenant isolation is the canonical `S:C` case**, and the sibling Portal *does* enforce the binding (`LicenseUploadService.cs:39`). **This changes the ordering of LicenseServer's four Highs: `NEW-5` is the most severe of them, not joint-third.**]* |
| **How to resolve** | **Effort: S.** read the `tenantId` claim from the validated token and require `claim == form["tenantId"]` at `:161`, and re-assert it at `:218-228` on validate. Then add authentication and bind the tenant to the authenticated principal (F-10). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-6 — Two divergent implementations of one licensing protocol share one root CA and one key, so the system's security is that of the weaker implementation

| Finding `NEW-6` | **Medium** · CVSS 3.1 **n/a — architectural aggregate, not additive** *(own vector computes 7.3; DO NOT ADOPT)* · component **LicenseServer** |
|---|---|
| **The issue** | Two divergent implementations of one licensing protocol share one root CA and one key, so the system's security is that of the weaker implementation |
| **Suggested fix** | Consolidate onto one implementation, or extract the validation contract into a single shared library with a conformance suite both implementations must pass. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[2026-09-09: CONFIRMED as an observation, and its computed 7.3 is DELIBERATELY NOT ADOPTED.** Every cell of the comparison table verified at source, and the load-bearing premise is now **measured**, not asserted: both implementations are anchored to the same root CA and unwrap with the same private key. The finding's central insight is valuable — **the Portal's compensating controls protect nothing an attacker can route around via the weaker implementation.** **But its CVSS is not supportable as an independent score in either direction:** `C:L/I:L/A:L` is a placeholder for "some of everything", and **every concrete impact this row names is already scored elsewhere in this register** — the missing tenant check is `NEW-5`, the forgeable assertion is `NEW-1`, the unauthenticated upload is `NEW-4`/`F-10`. **Promoting it to High 7.3 would add a fifth LicenseServer High whose exploitable content is entirely contained in the other four. That is not an up-score; it is double-counting the estate, and it would inflate a customer-facing High count.** Qualifier, on the row: *architectural aggregate — its impact is the union of `NEW-1`, `NEW-4` and `NEW-5` and is deliberately not scored additively; the independent contribution is that the Portal's compensating controls are void under a shared trust anchor.*] |
| **How to resolve** | **Effort: L.** consolidate onto one implementation and retire the other, or — if both must exist — extract the validation contract into a single shared library (as `License.Common` already is for the Portal) so that a control added in one place applies in both, and add a conformance test suite that both must pass. In the interim, bring this server to parity: set `ValidateAudience = true` with an explicit `ValidAudience` at `:152` and `:207`, add the tenant-claim check (NEW-5), add the domain binding, and add the modulus comparison at `:283-287`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-7 — EOL runtime, beyond the version number: floating package ranges with no lock file on an unsupported feed, an unpatchable base image rebuilt on every push, and `EnsureCreated()` binding the service to permanent DDL/`sa` privileges against a system database

| Finding `NEW-7` | **Medium** · CVSS 3.1 **6.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L` · component **LicenseServer** |
|---|---|
| **The issue** | EOL runtime, beyond the version number: floating package ranges with no lock file on an unsupported feed, an unpatchable base image rebuilt on every push, and `EnsureCreated()` binding the service to permanent DDL/`sa` privileges against a system database |
| **Suggested fix** | Move to a supported LTS runtime and base image, pin exact package versions with `packages.lock.json` and `RestoreLockedMode`, replace `EnsureCreated()` with versioned migrations, and drop the `sa` credentials. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[2026-09-09: `A:H` to `A:L`, 6.9 to 6.3, band Medium. Round 1 listed this as a Medium-to-High crosser at 7.6; re-derived at source it does NOT cross — it goes DOWN.** Every factual claim confirmed exactly (six floating `6.0.*` ranges; **0 lock/SBOM files against a positive control of 8 `.csproj` files**; `net6.0`; `sdk:6.0`/`aspnet:6.0`; `EnsureCreated()` at `:98`; `sa` against the `master` system database). **`A:H` fails because it rests on one inference the reviewer themselves marked `[UNVERIFIED — not executed]`** — that `EnsureCreated()` creates nothing against `master` so the compose stack fails at first query. **A metric at its maximum cannot rest on an unverified inference**, and the holds forbid executing it. **Framing: this row is a posture aggregate, not a single exploitable defect. Adopting 7.6 would have promoted "the runtime is EOL and the packages float" above four concrete, individually exploitable Highs in the same component** — a real distortion of the remediation queue produced entirely by arithmetic nobody had checked. **NOT TESTED: specific CVEs against EF Core 6.0.x, `System.IdentityModel.Tokens.Jwt` 6.36.0 and jose-jwt 5.2.0 — no network, so advisory data was not consulted and the verifier declined to guess.**] |
| **How to resolve** | **Effort: M.** move to a supported LTS runtime and base image; pin exact package versions and commit `packages.lock.json` with `RestoreLockedMode` in CI; add image scanning and an SBOM step; replace `EnsureCreated()` with versioned `Migrate()` and a real migrations project (the sibling already has one, per provider); create a dedicated application database and a least-privilege SQL login with `db_datareader`/`db_datawriter` only, applying schema changes out-of-band; remove the hardcoded `sa` credentials from `docker-compose.yml:7,23`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-8 — This repository has no secret-exclusion policy and no secret scanning at all, while its sibling has both

| Finding `NEW-8` | **Medium** · CVSS 3.1 5.3 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` · component **LicenseServer** |
|---|---|
| **The issue** | This repository has no secret-exclusion policy and no secret scanning at all, while its sibling has both |
| **Suggested fix** | Add a real `.gitignore` and a secret-scanning workflow wired as a required status check and a `needs:` dependency of the deploy job, with binary-aware scanning given `NEW-3`. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed outright — vector and score both exact. Measured: `.gitignore` is **one line** (`.DS_Store`); `.github/workflows/` holds **exactly one file**, read in full, with no gitleaks/CodeQL/dependency/image scan. **`C:L` is the right non-double-counting choice** — the key *exposures* are `NEW-2`, `NEW-3` and `F-11`; this row scores the process gap.]* |
| **How to resolve** | **Effort: S.** add a real `.gitignore`; add a gitleaks (or Defender/CodeQL) workflow **wired as a required status check** and as a `needs:` dependency of the deploy job; add binary-aware scanning given NEW-3; pin actions to SHAs; move `sa` credentials and the key file out of compose into secrets. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-9 — Generator hygiene: no operator authentication, no minting audit, predictable certificate serials, no certificate extensions, DN injection, no transport verification

| Finding `NEW-9` | **Medium** · CVSS 3.1 **4.6** `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:N` · component **LicenseServer** |
|---|---|
| **The issue** | (Low) — Generator hygiene: no operator authentication, no minting audit, predictable certificate serials, no certificate extensions, DN injection, no transport verification |
| **Suggested fix** | Move signing behind an authenticated, audited service backed by Key Vault or an HSM so the Generator submits a request rather than holding the key; in the interim, validate the tenant GUID, randomise serials and add certificate extensions. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[LOW to MEDIUM 4.6, 2026-09-09. Every metric supportable.** `Form1.cs:102-119` mints the device cert with **no extensions** — confirmed at source, **and by an idiom control** (the root generator adds three `CertificateExtensions.Add` calls; every leaf/device generator adds none), **and at the artefact level** (the sample's leaf shows no X509v3 block). `:106` serial = `BitConverter.GetBytes(DateTime.UtcNow.Ticks)`; `:103` DN from a free-text field; `:174,180` `new HttpClient()` with the comment *"assume system trust for demo"* in a tool that carries the root CA private key. `generate_license.py:30` uses `x509.random_serial_number()` — the correct behaviour both C# generators miss. **`AV:L` is correct and deliberate** (minting happens in a desktop WinForms application). **Read beside License-Services `NEW-9` — same defect class, different band, and the difference is stated there rather than left to look like a slip.**] |
| **How to resolve** | **Effort: M.** move signing behind an authenticated, audited service backed by Key Vault/HSM — the Generator should submit a request, not hold the key. In the interim: validate the tenant GUID, escape DN components, use `RandomNumberGenerator.GetBytes(16)` for serials, add `basicConstraints CA:FALSE` + `keyUsage` + EKU + a tenant SAN, pin the upload endpoint's certificate, and log every issuance. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/licenseserver-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-10 — What the committed sample licence tells us, and what it does not

| Finding `NEW-10` | **Info** · no CVSS score recorded · component **LicenseServer** |
|---|---|
| **The issue** | (Informational) — What the committed sample licence tells us, and what it does not. |
| **Suggested fix** | Remove the committed sample licence from the repository and treat it as disclosed. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed — the verifier decoded the sample themselves (`alg RS256`; claims exactly `deviceCertPem, encKeyBlob, exp, iat, iss, iss_to, maxDevices, tenantId`; leaf `CN=DatasecDevStaging`, 20-byte serial, **no extensions block**). **But its "it is expired, so it cannot itself be re-uploaded" reads as more reassurance than it is:** true for `NEW-4`/`NEW-5`, and **false for `NEW-1`** — the expired sample still unwrapped, because nothing on the forgery path consults `exp`.]* |
| **How to resolve** | Delete the committed sample licence, treat it and every artefact derivable from it as disclosed, and add `*.jwt` to the repository's exclusions alongside the key material of `NEW-8`. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### NEW-11 — No `ValidAlgorithms` allow-list

| Finding `NEW-11` | **Info** · no CVSS score recorded · component **LicenseServer** |
|---|---|
| **The issue** | (Informational) — No `ValidAlgorithms` allow-list. |
| **Suggested fix** | Configure an explicit `ValidAlgorithms` allow-list on both validators. |
| **What was tested** | The **LicenseServer** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/licenseserver-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed for **both** `NEW-11` rows. The reviewer's control re-run and it **fires**: `ValidAlgorithms` returns **zero hits** across both trees; positive control `ValidateIssuerSigningKey` returns **exactly 3 hits at the three cited validators**.]* |
| **How to resolve** | Set `ValidAlgorithms` explicitly on both validators. The verification pass confirmed the absence for both `NEW-11` rows with one control across the two trees, so one change closes both. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-UP-01 — The shared "hardened auth WebView" helper enables remote WebView debugging unconditionally, including on the WebView into which plaintext Entra admin credentials are typed

| Finding `D-UP-01` | **Informational** · CVSS 3.1 **n/a — latent, no reachable path** · component **UniversalPrint** |
|---|---|
| **The issue** | The shared "hardened auth WebView" helper enables remote WebView debugging unconditionally, including on the WebView into which plaintext Entra admin credentials are typed |
| **Suggested fix** | Delete the unconditional `setWebContentsDebuggingEnabled(true)` from the dead helper rather than leaving it as a trap for whoever wires the helper up: the call is process-global and would override both correct guards. |
| **What was tested** | The **UniversalPrint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/universalprint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[MEDIUM 6.1 to INFORMATIONAL (latent), 2026-09-09 — REFUTED AS FILED: the file it describes is DEAD CODE.** `util/webkit/AuthWebViewHardening.kt` is **never called from anywhere in UniversalPrint**: `configureHardenedAuthWebView` across the entire tree returns **exactly one occurrence — its own definition**; *(positive control, same tree and command form: `fillPassword` returns a definition **and** a live call site, so the grep finds call sites when they exist)*. `setWebContentsDebuggingEnabled(true)` at `:66` is real and unguarded but **never executes**, and the two "additional unconditional call-sites" are **both correctly guarded** (`AdminConsentActivity.kt:99`, `RegisterPrinterAuthActivity.kt:117-124`); the WebView that actually receives the admin credentials builds itself inline and never enables debugging. **Kept in full as a latent trap worth deleting** — `setWebContentsDebuggingEnabled` is process-global, so wiring the helper up would silently override both correct guards.] |
| **How to resolve** | Delete line 66 of `AuthWebViewHardening.kt` and the two call-sites at `AdminConsentActivity.kt:120` and `RegisterPrinterAuthActivity.kt:129`; if a debug affordance is needed, gate it on `BuildConfig.DEBUG` **and** verify the release APK's merged behaviour. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/universalprint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-UP-02 — The auth-WebView origin allow-list returns `true` for `javascript:`, `data:`, `blob:` and `about:` URIs before it applies the HTTPS/host test

| Finding `D-UP-02` | **Informational** · CVSS 3.1 **n/a — latent, no reachable path** · component **UniversalPrint** |
|---|---|
| **The issue** | The auth-WebView origin allow-list returns `true` for `javascript:`, `data:`, `blob:` and `about:` URIs before it applies the HTTPS/host test |
| **Suggested fix** | Apply the HTTPS test first and delete the `javascript:`, `data:` and `blob:` exemptions, and scope the localhost exemption to the caller that actually uses a localhost redirect. |
| **What was tested** | The **UniversalPrint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/universalprint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[MEDIUM 5.3 to INFORMATIONAL (latent), 2026-09-09 — REFUTED AS FILED, same dead file as `D-UP-01`.** The permissive-scheme ordering at `:81-83` is exactly as described, **in code nothing calls.** **AND THE TRUTH IS WORSE THAN THE FINDING: the reviewer called this predicate "the sole gate" for all three auth WebViews — it is not the sole gate, there is NO gate.** All three run with `javaScriptEnabled = true` and **none** implements `shouldInterceptRequest` or any origin allow-list, including `WebViewAutomatedLogin.kt:138`, the one that receives the printer admin password by `evaluateJavascript`. **Seat C proposes this be filed as a NEW UniversalPrint row and deliberately left unscored** (no off-origin navigation path has been established, and inventing one to justify a number is the failure this round exists to correct). **Creating a finding is outside this consolidation's authority — held for Tuesday, §2.3.7 open item 1.**] |
| **How to resolve** | Move the HTTPS check first and delete the `javascript`/`data`/`blob` exemptions (`about:blank` can be permitted explicitly by full-URI match if the teardown path needs it). Scope the `localhost`/`127.0.0.1` exemption to the caller that actually uses a localhost redirect, by passing `redirectHost` rather than hard-coding the hosts. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/universalprint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-UP-03 — IPP certificate "pinning" derives its trust anchor from an unauthenticated fetch performed by a deliberately obfuscated trust-all TrustManager

| Finding `D-UP-03` | **Medium** · CVSS 3.1 4.2 · component **UniversalPrint** |
|---|---|
| **The issue** | IPP certificate "pinning" derives its trust anchor from an unauthenticated fetch performed by a deliberately obfuscated trust-all TrustManager |
| **Suggested fix** | Pin to the certificate captured at printer registration and already stored in `EncryptedSharedPreferences`, and delete the reflective trust-all indirection so the trust decision is visible to reviewers and tooling. |
| **What was tested** | The **UniversalPrint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/universalprint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed at 4.2; the reviewer's bounding of the impact is careful and correct. **One wording correction:** the row states the literals `checkServerTrusted`, `X509TrustManager` and `getAcceptedIssuers` "therefore never appear in the binary". **`X509TrustManager` does appear** — `PrinterNetworkHelper.kt:19` imports it and the file casts `as X509TrustManager`, so the type is in the constant pool. **The method-name claim stands; the type-name claim does not.** This matters because it is the sentence a customer assurance reader would test first.]* |
| **How to resolve** | Pin to the certificate captured during printer registration and stored in `EncryptedSharedPreferences` (the app already stores per-printer certs — `common/SecuredPreferences.kt`), not to a freshly-fetched one. Delete the reflective indirection in `PrinterNetworkHelper.kt:33-53` so that the trust decision is visible to reviewers and to tooling; if a trust-all fetch is genuinely required for enrolment, make it explicit and confine it to that one call. **Record the anti-analysis obfuscation against F-03** — a customer assurance review will ask why it is there. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/universalprint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-UP-04 — Admin-consent OAuth request carries no `state` parameter (dead statement), and the tenant id is harvested from the redirect URL and persisted with no binding

| Finding `D-UP-04` | **Medium** · CVSS 3.1 **5.3** `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:H/A:N` · component **UniversalPrint** |
|---|---|
| **The issue** | Admin-consent OAuth request carries no `state` parameter (dead statement), and the tenant id is harvested from the redirect URL and persisted with no binding |
| **Suggested fix** | Generate, assign, persist and check a cryptographically random `state`, and apply the same fix to MailFlow. |
| **What was tested** | The **UniversalPrint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/universalprint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed exactly (`AdminConsentActivity.kt:86` is a bare map read between two assignments — a dead expression statement; `:152-162` persists the harvested tenant with no binding check). `C:L` to `C:N`: nothing is disclosed and the OAuth authority is a resource constant, so no token is redirected. 4.7 to 5.3, band unchanged.]* |
| **How to resolve** | Generate a cryptographically random `state`, **assign** it into `queryParams`, persist it for the flow's duration, and reject any redirect whose `state` does not match. Apply the same fix to MailFlow. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/universalprint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-UP-05 — OnGuardLib native app-integrity gate is disabled: `isApplicationAuthorized` returns hardcoded `true`, and four of six JNI call-sites are additionally commented out

| Finding `D-UP-05` | **Medium** · CVSS 3.1 6.2 · component **UniversalPrint** |
|---|---|
| **The issue** | OnGuardLib native app-integrity gate is disabled: `isApplicationAuthorized` returns hardcoded `true`, and four of six JNI call-sites are additionally commented out |
| **Suggested fix** | Un-comment the gate call and the four JNI call sites, implement F-13's signature check, and verify by asserting the gate returns `false` for an unauthorised caller. |
| **What was tested** | The **UniversalPrint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/universalprint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: confirmed at 6.2 (`auth.cpp:8-12` — the gate returns hardcoded `true`). **The aggravator is REFUTED and should not be carried:** "four of six JNI call-sites additionally commented out" is **true but adds nothing to severity** — since `isApplicationAuthorized` returns `true` unconditionally, commenting out its call sites has **zero functional effect**. It is evidence of fork divergence (`D-UP-06`), not additional exposure.]* |
| **How to resolve** | Un-comment `auth.cpp:10` and `locker.cpp:34,62,90,117`, implement F-13's signature check inside `isApplicationPackageGenuine`, and verify by asserting `isApplicationAuthorized` returns `false` for an unauthorised caller — not by inspecting the presence of the check. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/universalprint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-UP-06 — Cross-cutting: five divergent private forks of OnGuardLib, which is why the same control is enabled in two apps and disabled in three

| Finding `D-UP-06` | **Low** · no CVSS score recorded · component **UniversalPrint** |
|---|---|
| **The issue** | Cross-cutting: five divergent private forks of OnGuardLib, which is why the same control is enabled in two apps and disabled in three. |
| **Suggested fix** | Consolidate OnGuardLib into one versioned artefact with a single JNI contract and per-app secrets supplied at build time rather than by forking the source. |
| **What was tested** | The **UniversalPrint** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/universalprint-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** *[2026-09-09: **confirmed for three of the five apps only.** The verifier read `auth.cpp` in MailFlow, CypherSharePoint and UniversalPrint — **all three have the gate off** — and UniversalPrint additionally has 4 of 5 `locker.cpp` call sites commented. **The CypherOneDrive and Teams columns of this finding's table were not opened** (another partition). So "enabled in two apps and disabled in three" rests on **three confirmations and two unverified**, and the row should say so.]* |
| **How to resolve** | Consolidate OnGuardLib into one versioned artefact with a single JNI contract, per-app secrets supplied at build time rather than by forking the source, and one place to verify the gate. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/universalprint-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-UP-07 — All three auth WebViews run with JavaScript enabled and have no origin allow-list and no sub-resource filtering at all — including the one that receives the printer administrator password

| Finding `D-UP-07` | **Medium** · CVSS 3.1 **n/a — control absence; no off-origin navigation path established** · component **UniversalPrint** |
|---|---|
| **The issue** | All three auth WebViews run with JavaScript enabled and have **no origin allow-list and no sub-resource filtering at all** — including the one that receives the printer administrator password |
| **Suggested fix** | Apply UniversalPrint's own origin predicate — with the `javascript:`, `data:` and `blob:` exemptions removed per `D-UP-02` — to all three auth WebViews, add sub-resource filtering, and disable JavaScript where the flow does not need it. |
| **What was tested** | The **UniversalPrint** component, as provided in the source snapshot. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2, across three disjoint partitions. Each verifier wrote a CVSS 3.1 implementation from the specification and validated it against published reference vectors **before** scoring, and re-derived the vector from source metric by metric rather than recomputing the filed one. **Test record.** **[NEW ROW, FILED 2026-09-09 on Tuesday's ruling — §2.3.7 open item 1b, ACCEPT. Raised by seat C (`round2-c.md` §2.2) and re-measured at source independently by the finalise seat.** The reviewer's original claim was that `isAllowedAuthUri` is *"the sole gate for both navigation and sub-resource loading in all three auth WebViews"*. **It is not the sole gate — there is no gate**, because the file it lives in is never called. **Measured across `UniversalPrint-main`:** `shouldInterceptRequest` returns **zero occurrences tree-wide** *(positive control, same command form: `onPageFinished` returns 9 hits across all three WebView clients — the instrument finds overrides when they exist, so the zero is a measurement)*; `configureHardenedAuthWebView` and `isAllowedAuthUri` occur **only inside `AuthWebViewHardening.kt` itself** (definitions at `:36` and `:74`, one internal call at `:72`) — **no external call site anywhere**; `javaScriptEnabled = true` at `AdminConsentActivity.kt:103`, `RegisterPrinterAuthActivity.kt:128` and `WebViewAutomatedLogin.kt:115`. `shouldOverrideUrlLoading` exists in two of the three and both `return super` with no origin test; **the credential-typing WebView has none.** **One refinement the finalise seat adds to seat C's account, because it makes the row more precise rather than louder:** the credential path is not wholly unguarded — `WebViewAutomatedLogin.kt:144` tests `url.contains("login.microsoftonline.com")` before injecting the username and password at `:255` and `:271`. **That is a substring test against the whole URL, not a host comparison**, so any URL merely containing that string satisfies it; and it gates only the credential injection, never the navigation. **DELIBERATELY UNSCORED, and that is this row's honest state.** No path that navigates these WebViews off-origin has been established, and inventing one to justify a number is the failure round 2 exists to correct. The band follows this register's own convention for a control that is **absent** rather than defeated (`I-D9`, `I-D10`, `H-D7`). **REVISIT GATE, written so evidence and not argument closes it:** trace whether anything can navigate any of the three off-origin. **If such a path exists this row is scored and will rise; if it is established that none can, it drops to Informational** beside `D-UP-01` and `D-UP-02`. **This row replaces `D-UP-02` as the live-code statement of the defect.** `D-UP-02` stays, correctly, Informational-latent — it describes dead code, and this describes code that runs. **Static analysis only. No device, no live pass.**] |
| **How to resolve** | UniversalPrint already contains the predicate this needs — `isAllowedAuthUri` — so this is applying an existing control rather than writing a new one. (1) Fix that predicate first per `D-UP-02`: apply the HTTPS test before the scheme exemptions and delete the `javascript:`, `data:` and `blob:` cases. (2) Apply it to all three auth WebViews, including the one that receives the printer administrator password. (3) Add `shouldInterceptRequest` so sub-resources are filtered by the same rule. (4) Disable JavaScript on any of the three that does not need it. **The row is deliberately unscored because no off-origin navigation path was established; the revisit gate is that trace, and it does not need a live system.** |

**Tally for this section: 4 Critical, 8 High, 31 Medium, 10 Low and 9 Informational, totalling 62
counted.** Re-added by column: 4 + 8 + 31 + 10 + 9 = 62. **Plus one withdrawn row, retained and not
counted: `D-MF-01`.** The table prints sixty-three rows and sixty-two are counted. The section total
is sixty-two on either side of the two 2026-09-09 changes by coincidence rather than by construction:
one row left the count and a different row entered it.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.7 Delta review, the components reviewed before the session limit

A gap that nobody had stated, found while filing §3.6 and reported rather than left. The commission
covered batch 1. Measuring it revealed that **the eight components delta-reviewed on 2026-09-07
before the session limit — the set previously listed as "done" — had unfiled findings too.** "Done"
meant *reviewed*, not *filed*. Leaving them out after finding them would have reproduced exactly the
defect the commission existed to fix, so they were filed.

Thirty-seven findings were filed across those eight components; **thirty-one belong to the HP
Authentication Suite and appear below.** The remaining six, all against Task-Dispatcher, are carried
in the companion Datasec register.

**Verification status: all rows have been independently re-derived at source** in two partitions.
**The defect this section actually had was not a wrong number; it was a band with nothing behind it.**
Twenty-seven of the thirty-seven rows printed an em-dash in the CVSS column while carrying a declared
band, and the vectors existed all along, written down in the delta files and dropped in transcription.
They are now recorded. A wrong number announces itself under arithmetic; a bare band does not, which
is why this was the worse of the two defects.

**Summary of the findings in this section.** The full record for each — the issue, the suggested fix, and below them what was tested, how it was tested and how to resolve it — follows the table, one finding to a block.

| ID | Component | Severity | CVSS 3.1 | Finding |
|---|---|---|---|---|
| DELTA-CC-01 | cc-api | Medium | **5.0** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:N/A:N` | HTTP parameter injection into the Keycloak Admin API via the unescaped plaintext-sequence fallback |
| DELTA-CC-02 | cc-api | Medium | **4.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L` | Uncontrolled resource consumption: Polly retries 5× with exponential back-off and retries on 404, with no rate limiting anywhere |
| DELTA-CC-03 | cc-api | Medium | **4.3 base** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` | `ConfigController` hands out the app config (including `LoggingSecret`) to any positional-realm caller; no per-caller realm binding — the F-08 authorisation… |
| DELTA-HP-01 | hpam-api | **WITHDRAWN 2026-09-09** *(was Low)* | **n/a — withdrawn; never a counted finding in its author's own words** | `send` relays an unvalidated, unbounded payload; no schema, no size cap (Low) |
| DELTA-HP-02 | hpam-api | **WITHDRAWN 2026-09-09** *(was Info)* | **n/a — withdrawn; never a counted finding in its author's own words** | raw error disclosure on `negotiate` and `send` (Informational — already in F-06 remediation) |
| DELTA-MK-01 | hpam-marketplace | Medium *(bucketed)* | **8.3 base** `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` — **held at Medium pending blob-ACL evidence** | Supply-chain: the License-Portal runtime is fetched at deploy time from a hardcoded public blob over the network with no integrity/signature check |
| DELTA-MK-02 | hpam-marketplace | **High** | **7.2** `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` | Storage account key written in cleartext to Function App settings while a SystemAssigned managed identity exists and is unused for storage |
| DELTA-MK-03a | hpam-marketplace | **Medium** | **4.9** `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:N/A:N` | Entra client secrets are written into App Service app-settings as cleartext, with no Key Vault reference |
| DELTA-MK-03b | hpam-marketplace | **Medium** | **4.3** `CVSS:3.1/AV:P/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N` | The marketplace UI collects those same client secrets in an unmasked text box, so they are typed and displayed in the clear |
| ~~DELTA-MK-03~~ | hpam-marketplace | **SPLIT 2026-09-09 — superseded by `DELTA-MK-03a` and `DELTA-MK-03b`** | *(see the two rows above)* | Client secrets persisted as cleartext app settings (no Key Vault reference); UI collects them in an unmasked TextBox |
| DELTA-MK-04 | hpam-marketplace | Low | **n/a — `[GAP]`, unscoreable from this repository** | License Portal deployed multi-tenant (`AzureAd__TenantId: 'common'`); tenant restriction delegated to an app-level `HomeTenantId` check that cannot be… |
| DELTA-MK-05 | hpam-marketplace | Low | **(a) Informational · (b) 4.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` | SignalR upstream `auth: { type: 'None' }` and deploymentScripts run with `--debug` (Low / Informational) |
| D-01 | HPAuthenticationManager | **Critical** | **9.2** `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` | Unauthenticated, implicitly-exported runtime broadcast receivers let any co-located app emulate a card tap and force sign-in / sign-out (bypasses the card… |
| D-02 | HPAuthenticationManager | **High** | **7.9** `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:L` | HPCC "Custom" cloud configuration re-points the OAuth authority, Graph and Monitor endpoints with no scheme or host validation; HPAM then re-broadcasts the… |
| D-03 | HPAuthenticationManager | **High** | 8.7 `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` | The complete HPCC configuration — including the tenant's Entra client secret and API key — is logged at INFO level on every config consume, and INFO-level… |
| D-04 | HPAuthenticationManager | Medium *(bucketed)* | **7.9 base** `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` | The token broker hands one union-scoped delegated Graph token to every consumer app, exposes the directory-stored refresh token and card blobs through… |
| D-05 | HPAuthenticationManager | Medium *(bucketed)* | **8.1 base** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` | Additional committed credentials not in F-16's inventory, sitting in the one directory the new gitleaks CI gate is configured to ignore |
| D-06 | HPAuthenticationManager | Medium | **5.5** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` | The runtime debug toggle also enables OkHttp `Level.BODY` logging on all three HTTP clients, dumping the client secret, all tokens and every Graph CSA… |
| D-07 | HPAuthenticationManager | **Informational** | **n/a — no reachable path in this snapshot** | `CloudConfigService.getConfig()` has no caller check while its sibling methods do |
| D-08 | HPAuthenticationManager | Low | — *(correctly unscored; `[UNVERIFIED impact]` tag now RESOLVED)* | Sign-in attributes passed to the Workpath platform contain a hardcoded password and placeholder external e-mail addresses |
| ADM-D1 | datasec-administration-portal | **High** | **7.5** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` | Marketplace webhook accepts an UNVERIFIED JWT: signature never checked, and the two claim values it compares are a public Microsoft constant and a committed… |
| ADM-D2 | datasec-administration-portal | Medium | **5.4** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:L` | `POST /api/saas` (representative create) has no ownership check: any Entra user in any tenant can pre-register the HP representative for any subscription id |
| ADM-D3a | datasec-administration-portal | Medium *(bucketed; base 7.1 recorded and deliberately NOT published as the band)* | **7.1 base** `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` | The provisioned Keycloak realm auto-links federated identities with both first-broker-login verification steps deleted, so an identity provider that asserts… |
| ADM-D3b | datasec-administration-portal | Medium *(reachability reduced by the Keycloak-retirement attestation; exploitability marked Suspected by the reviewer — both qualifiers survive the split, per seat D)* | **n/a — configuration weakness; no attack path established from this repository** | The provisioned public client `HP-Secure-Authentication` has the OAuth 2.0 implicit flow enabled, so tokens are returned through the front channel to a… |
| ADM-D3c | datasec-administration-portal | Medium *(reachability reduced by the Keycloak-retirement attestation; exploitability marked Suspected by the reviewer — both qualifiers survive the split, per seat D)* | **n/a — configuration weakness; no attack path established from this repository** | The same public client has direct access grants (the resource-owner password credentials grant) enabled, so end-user passwords are presented directly to a… |
| ADM-D3d | datasec-administration-portal | Medium *(reachability reduced by the Keycloak-retirement attestation; exploitability marked Suspected by the reviewer — both qualifiers survive the split, per seat D)* | **n/a — configuration weakness; no attack path established from this repository** | The same public client is provisioned with wildcard web origins, so any web origin is permitted to make browser calls on its behalf |
| ADM-D3e | datasec-administration-portal | Low *(reachability reduced by the Keycloak-retirement attestation; exploitability marked Suspected by the reviewer — both qualifiers survive the split, per seat D)* | **n/a — a session-lifetime posture, not an attack path** | Every provisioned realm is created with an SSO session idle timeout and maximum lifespan of exactly 180 days, neither settable per realm |
| ~~ADM-D3~~ | datasec-administration-portal | **SPLIT 2026-09-09 — superseded by `ADM-D3a` … `ADM-D3e`** | *(see the five rows above)* | The Keycloak realm the portal provisions has a weak trust posture: unverified automatic account-linking, a public client with implicit + password grants and… |
| ADM-D4 | datasec-administration-portal | Low *(bucketed "environmentally Low")* | **8.1 base** `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` | Front-end lockfile is deliberately git-ignored and CI `npm install`s unpinned ranges straight into the production artefact; the "Build, Test and Deploy"… |
| ADM-D5 | datasec-administration-portal | **Medium** | **5.3** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N` | Event Grid validation handshake and delivery-report ingestion trust the body once the (committed) code is presented |
| QA-D1 | QuickAccessLibrary | Low | **3.1** `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N` | Library fetches a host-supplied thumbnail URL with no scheme/host constraint (June lead, still unscored) |
| QA-D2 | QuickAccessLibrary | Info | — | Informational: dependency currency of the only network-capable component |
| WP-D1 | WorkPathApplications | Low *(bucketed "env-adjusted")* | **5.3** `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N` | The repository is a secret-bearing archive in a format its own secret-scanning CI cannot inspect |
| WP-D2 | WorkPathApplications | Info | — | Informational: `restore_from_bundles.sh` chunked-bundle path uses an undeclared associative array |
| WP-D3 | WorkPathApplications | Info | — | Informational: workflow pinning |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-CC-01 — HTTP parameter injection into the Keycloak Admin API via the unescaped plaintext-sequence fallback

| Finding `DELTA-CC-01` | **Medium** · CVSS 3.1 **5.0** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:N/A:N` · component **cc-api** |
|---|---|
| **The issue** | HTTP parameter injection into the Keycloak Admin API via the unescaped plaintext-sequence fallback |
| **Suggested fix** | URL-encode the fallback sequence value exactly as the encrypted branch does, and per F-04 remove the plaintext retry entirely. |
| **What was tested** | The **cc-api** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/cc-api-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed at source, band holds; two metrics moved and they nearly cancel. `KeycloakService.cs:139` escapes the encrypted branch while **`:145` interpolates the caller's raw `sequence` with no encoding**, and `IKeycloakClient.cs:21-23` declares `[QueryUriFormat(UriFormat.Unescaped)]` so Refit adds none either. **`AC:H` to `AC:L`: the reviewer used `AC:H` to express uncertainty about the exploit ceiling, which is not what `AC` measures.** The delta file's "≈4.7" is not what its own vector produces (4.9); re-derived, 5.0.]* |
| **How to resolve** | URL-encode the fallback value (`Uri.EscapeDataString(sequence)`) exactly as the encrypted branch does, or remove `[QueryUriFormat(UriFormat.Unescaped)]` and let Refit encode; and per F-04, remove the plaintext retry entirely. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cc-api-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-CC-02 — Uncontrolled resource consumption: Polly retries 5× with exponential back-off and retries on 404, with no rate limiting anywhere

| Finding `DELTA-CC-02` | **Medium** · CVSS 3.1 **4.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L` · component **cc-api** |
|---|---|
| **The issue** | Uncontrolled resource consumption: Polly retries 5× with exponential back-off **and retries on 404**, with no rate limiting anywhere |
| **Suggested fix** | Remove `.OrResult(NotFound)` from the retry predicate, cap the total retry duration, and add rate limiting on the public controllers. |
| **What was tested** | The **cc-api** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/cc-api-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed at source, band holds; **`A:H` to `A:L`**, 6.5 to 4.3.]* |
| **How to resolve** | Remove `.OrResult(NotFound)` from the retry predicate; cap total retry duration; add ASP.NET Core rate limiting (`AddRateLimiter`) on the public controllers. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cc-api-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-CC-03 — `ConfigController` hands out the app config (including `LoggingSecret`) to any positional-realm caller; no per-caller realm binding — the F-08 authorisation class extends past UsersController

| Finding `DELTA-CC-03` | **Medium** · CVSS 3.1 **4.3 base** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` · component **cc-api** |
|---|---|
| **The issue** | `ConfigController` hands out the app config (including `LoggingSecret`) to any positional-realm caller; no per-caller realm binding — the F-08 authorisation class extends past UsersController |
| **Suggested fix** | Apply F-08's realm-binding fix to every `[Authorize]` controller rather than to `UsersController` alone, and stop returning `LoggingSecret` to clients. |
| **What was tested** | The **cc-api** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/cc-api-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed-with-wording. **`C:H` is aggravator-dependent, so the base is scored at `C:L`** (6.5 to 4.3); the title mis-describes the defect. Band holds Medium.]* |
| **How to resolve** | The F-08 fix (assert route `realm` == token realm claim; add role policies) must be applied to **all** `[Authorize]` controllers, not just Users; and `LoggingSecret` should never be returned to clients — move debug-logging control server-side. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/cc-api-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-HP-01 — `send` relays an unvalidated, unbounded payload; no schema, no size cap (Low)

| Finding `DELTA-HP-01` | **WITHDRAWN 2026-09-09** *(was Low)* · CVSS 3.1 **n/a — withdrawn; never a counted finding in its author's own words** · component **hpam-api** |
|---|---|
| **The issue** | `send` relays an unvalidated, unbounded payload; no schema, no size cap |
| **Suggested fix** | **Withdrawn — de-counted, not deleted.** No severity attaches, but the observation stands: `send` should take a schema and a size cap. |
| **What was tested** | The **hpam-api** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpam-api-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[2026-09-09: confirmed as code, and the row raises a COUNTING question this consolidation refused to decide.** `send.js:12` is `authLevel: 'anonymous'` and `:16-21` fans the **entire** request body out to a caller-named `realm` target with no size limit and no schema. `PR` cannot be determined from code — all three functions are anonymous and the only gate is App Service Easy Auth applied **out of band by a deploy script**, which is a live check and is **held**. Both defensible readings are **Medium** (`PR:L` `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:L` = 5.4 with Easy Auth on; `PR:N` = 6.5 with it off). **BUT the delta file's own §1 opens "None rise to a new scored finding" and calls `DELTA-HP-01` and `DELTA-HP-02` "honest sub-observations … not as a new finding". The register counts both as findings anyway.** The author's own statement did not survive transcription. **WITHDRAWN 2026-09-09 on Tuesday's ruling — §2.3.7 open item 1e, ACCEPT as a MARKED WITHDRAWAL.** **THE ROW IS NOT DELETED.** It stays here, marked withdrawn, carrying the author's own statement that refuted its status, and it leaves the counted total and the tallies only (§2.3.4 Low −1). **This is a withdrawal of a COUNTING error, not of the observation.** The code is exactly as described and `send.js` remains anonymous, unbounded and schema-less; what was wrong was the register counting as a finding something its author explicitly filed as a sub-observation. **The observation is retained in full above and should still be fixed.** The Easy Auth revisit gate stays open and is a live check, which is held.] |
| **How to resolve** | No remediation attaches to a withdrawn row. **The observation is not withdrawn:** `send` still relays an unvalidated, unbounded payload with no schema and no size cap, and it should take both. What was withdrawn is its place in the count — its author's own working file recorded it *"not as a new finding"* and the register had counted it anyway. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-HP-02 — raw error disclosure on `negotiate` and `send` (Informational — already in F-06 remediation)

| Finding `DELTA-HP-02` | **WITHDRAWN 2026-09-09** *(was Info)* · CVSS 3.1 **n/a — withdrawn; never a counted finding in its author's own words** · component **hpam-api** |
|---|---|
| **The issue** | raw error disclosure on `negotiate` and `send`. |
| **Suggested fix** | **Withdrawn — de-counted, not deleted.** The raw error disclosure is real and is already carried by F-06's remediation. |
| **What was tested** | The **hpam-api** component, as provided in the source snapshot. The claim under test: *raw error disclosure on `negotiate` and `send` (Informational — already in F-06 remediation)*. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpam-api-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed exactly (`printerhub.js:18-21` returns the raw error object; `send.js:28-31` returns `error.message`). **Correctly Informational, and a duplicate of an existing remediation item, not a new defect** — the delta file says so itself. **WITHDRAWN 2026-09-09 on Tuesday's ruling (§2.3.7 open item 1e, ACCEPT as a MARKED WITHDRAWAL): the row is retained and marked, and leaves the count only (§2.3.4 Informational −1). The raw error disclosure is real and still worth fixing; it was never a new finding.**]* |
| **How to resolve** | No remediation attaches to a withdrawn row. **The observation is not withdrawn:** the raw error disclosure on `negotiate` and `send` is real, and it is already carried by F-06's remediation, which is where it should be fixed. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-MK-01 — Supply-chain: the License-Portal runtime is fetched at deploy time from a hardcoded public blob over the network with no integrity/signature check

| Finding `DELTA-MK-01` | **Medium *(bucketed)*** · CVSS 3.1 **8.3 base** `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` — **held at Medium pending blob-ACL evidence** · component **hpam-marketplace** |
|---|---|
| **The issue** | Supply-chain: the License-Portal runtime is fetched at deploy time from a hardcoded public blob over the network with **no integrity/signature check** |
| **Suggested fix** | Ship the licence zip the way the API stack does, or pin and verify a SHA-256 of the download before deploying, and make the blob container private. |
| **What was tested** | The **hpam-marketplace** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpam-marketplace-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed at source and **the bucketing is CORRECT and deliberately preserved.** `license/main.bicep:21,294` — a hardcoded public blob URL fetched with `curl -L` and `az webapp deployment source config-zip`, with **no checksum, hash pin or signature**; the sibling API stack uses `loadFileAsBase64` instead, so the two stacks differ and the license stack took the weaker pattern. **Control fires:** `sha256\|sha512\|checksum\|md5\|signature\|gpg\|cosign\|digest\|hash` across every `*.bicep`/`*.json`/`*.sh` returns **exactly two hits, both Bicep's own `templateHash` build metadata.** `UI:N` to `UI:R` (the poisoned blob pays out only when a customer runs the marketplace deployment). **Three separate figures previously existed for this row — band Medium, a stated "≈8.1", and a vector-implied 9.0 — and the register published none of them. All three are now reconciled: 8.3 base, held at Medium.** **THE SEVERITY GATE IS ONE LIVE COMMAND AND IT IS HELD:** the ACL of the `datasecsolutions` storage account and the `hpam-license` container. **If that container is writable by anything other than a tightly-held publish identity, this is a Critical-adjacent supply-chain defect reaching every customer tenant that deploys the offer.** It is the single highest-value unblocking question in this component.]* |
| **How to resolve** | Ship the license zip via `loadFileAsBase64` like the API stack, or pin+verify a SHA-256 of the download before deploying; ensure the blob container is private and the account is Deny-by-default (mirroring F-29 remediation). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpam-marketplace-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-MK-02 — Storage account key written in cleartext to Function App settings while a SystemAssigned managed identity exists and is unused for storage

| Finding `DELTA-MK-02` | **High** · CVSS 3.1 **7.2** `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` · component **hpam-marketplace** |
|---|---|
| **The issue** | Storage **account key** written in cleartext to Function App settings while a SystemAssigned managed identity exists and is unused for storage |
| **Suggested fix** | Use identity-based storage connections — grant the site's managed identity `Storage Blob Data Owner` and drop the account key — and set `allowSharedKeyAccess:false`. |
| **What was tested** | The **hpam-marketplace** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpam-marketplace-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[MEDIUM to HIGH 7.2, 2026-09-09.** `bicep/main.bicep:206-207` declares a SystemAssigned identity and **never uses it for storage**, while `:332-333` build both storage settings from `listKeys().keys[0].value` — **the shared account key, cleartext, in site app-settings** — and `:96,100,105` leave `publicNetworkAccess: 'Enabled'`, `allowSharedKeyAccess: true` and `networkAcls.defaultAction: 'Allow'`, **so the key is usable from anywhere on the internet.** **`AC:H` to `AC:L`** (reading site app-settings is a single ARM call for anyone holding the role; `AC:H` was doing the job `PR:H` already does). **`A:N` to `A:H`** — a Storage **shared account key** is read/write/**delete** across the whole data plane, and the account holds `AzureWebJobsStorage` and the deployment container. `S:U` retained **deliberately**: the Function App and the storage account are two resources under one Azure RBAC authority, and consistency was preferred over the extra 0.9 an `S:C` would have bought. **THE FINDING IS ALSO UNDER-STATED:** `:331` writes **`SIGNALR_CONNECTION_STRING: hpamSignalR.listKeys().primaryConnectionString`** — a *second* cleartext service credential two lines above the one the finding names, granting full control of the hub. The row's title should read "storage account key **and SignalR primary connection string**", and it compounds with `DELTA-MK-05`'s unauthenticated SignalR upstream.**]** |
| **How to resolve** | Use identity-based storage connections (drop the `AccountKey=…` connection strings; grant the site MI `Storage Blob Data Owner`), set `allowSharedKeyAccess:false` (F-29). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpam-marketplace-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-MK-03a — Entra client secrets are written into App Service app-settings as cleartext, with no Key Vault reference

| Finding `DELTA-MK-03a` | **Medium** · CVSS 3.1 **4.9** `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:N/A:N` · component **hpam-marketplace** |
|---|---|
| **The issue** | Entra client secrets are written into App Service app-settings as cleartext, with no Key Vault reference |
| **Suggested fix** | Store the client secrets as Key Vault references rather than as cleartext application settings. |
| **What was tested** | The **hpam-marketplace** component, as provided in the source snapshot. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[SPLIT OUT OF `DELTA-MK-03` ON TUESDAY'S RULING 2026-09-09 — §2.3.7 open item 1c, ACCEPT. It was half of one `Low`; on its own vector it is a Medium.** Confirmed at source: `bicep/main.bicep:333` writes `MICROSOFT_PROVIDER_AUTHENTICATION_SECRET: appClientSecret` straight into site app-settings with no `@Microsoft.KeyVault(...)` reference, and `license/main.bicep:216-218` does the same for `AzureAd__ClientSecret`. **The reviewer's `securestring` mitigation is real but does not support a `Low`, and this is the half it supports least:** `securestring` keeps the value out of deployment history and activity logs; it does nothing whatever about a value sitting cleartext at rest in site config, readable by any principal holding site-config read. **This is the half that carries the remediation that matters — Key Vault references — which is precisely why the verifier asked for the split rather than a re-band.** **NOT TESTED:** whether any deployed tenant restricts site-config read; whether the Entra app carries a certificate credential or a conditional-access constraint. **Static analysis only. No secret value, prefix or length was read from any file.**] |
| **How to resolve** | Store the secrets as Key Vault references rather than as cleartext application settings. This is the first half of the parent row `DELTA-MK-03`'s remediation, split so that the two halves can be scheduled separately. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-MK-03b — The marketplace UI collects those same client secrets in an unmasked text box, so they are typed and displayed in the clear

| Finding `DELTA-MK-03b` | **Medium** · CVSS 3.1 **4.3** `CVSS:3.1/AV:P/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N` · component **hpam-marketplace** |
|---|---|
| **The issue** | The marketplace UI collects those same client secrets in an unmasked text box, so they are typed and displayed in the clear |
| **Suggested fix** | Use a masked input for the secret in `createUiDefinition`. |
| **What was tested** | The **hpam-marketplace** component, as provided in the source snapshot. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[SPLIT OUT OF `DELTA-MK-03` ON TUESDAY'S RULING 2026-09-09 — §2.3.7 open item 1c, ACCEPT.** Measured across both UI definitions: **`Microsoft.Common.PasswordBox` appears 0 times against `Microsoft.Common.TextBox` 8 times (API) and 6 times (license)** — the control that exists for exactly this purpose is used nowhere. **Why one score could never have described both halves:** this one is physical shoulder-surfing at the moment of entry (`AV:P`, `UI:R`); `DELTA-MK-03a` is a network-reachable at-rest disclosure gated by an Azure role (`AV:N`, `PR:H`). Different attacker, different vector, different remediation. **Static analysis only. No secret value, prefix or length was read.**] |
| **How to resolve** | Use a masked input in `createUiDefinition`. This is the second half of the parent row `DELTA-MK-03`'s remediation, split so that the two halves can be scheduled separately. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-MK-03 — Client secrets persisted as cleartext app settings (no Key Vault reference); UI collects them in an unmasked TextBox

| Finding `DELTA-MK-03` | **SPLIT 2026-09-09 — superseded by `DELTA-MK-03a` and `DELTA-MK-03b`** · CVSS 3.1 *(see the two rows above)* · component **hpam-marketplace** |
|---|---|
| **The issue** | **ROW RETAINED, NOT DELETED, AND NOT COUNTED — it is the parent of the two rows above, kept so the split is auditable.** Original text and evidence: Client secrets persisted as cleartext app settings (no Key Vault reference); UI collects them in an unmasked TextBox |
| **Suggested fix** | Superseded by the two rows above; the fixes are recorded on `DELTA-MK-03a` and `DELTA-MK-03b`. |
| **What was tested** | The **hpam-marketplace** component, as provided in the source snapshot. The claim under test: *Client secrets persisted as cleartext app settings (no Key Vault reference); UI collects them in an unmasked TextBox*. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpam-marketplace-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[PARTLY REFUTED 2026-09-09 — this is TWO defects sharing one ID, and they belong in different bands.** (a) cleartext client secret at rest in site config, `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:N/A:N` = **4.9**; (b) unmasked entry / shoulder-surf, `CVSS:3.1/AV:P/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N` = **4.3**. Both confirmed at source: `bicep/main.bicep:333` and `license/main.bicep:216-218` write the secret straight to app-settings with no `@Microsoft.KeyVault(...)` reference, and **`Microsoft.Common.PasswordBox` appears 0 times against `Microsoft.Common.TextBox` 8 and 6 times** in the two UI definitions. **The reviewer's `securestring` mitigation does not support the `Low` band, because it addresses a third thing** — it stops the secret entering deployment history and activity logs, and does nothing about either defect actually filed. **Neither half is a Low on its own vector.** **The verifier's recommendation is not "make it a Medium" — it is to SPLIT the row and let the at-rest half carry the Key Vault remediation. Splitting creates a finding, which this consolidation was not authorised to do: the row stands as one Low and the split is held for Tuesday (§2.3.7 open item 1).**] |
| **How to resolve** | Store secrets as Key Vault references; use a masked input in createUiDefinition. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpam-marketplace-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-MK-04 — License Portal deployed multi-tenant (`AzureAd__TenantId: 'common'`); tenant restriction delegated to an app-level `HomeTenantId` check that cannot be verified from IaC

| Finding `DELTA-MK-04` | **Low** · CVSS 3.1 **n/a — `[GAP]`, unscoreable from this repository** · component **hpam-marketplace** |
|---|---|
| **The issue** | License Portal deployed multi-tenant (`AzureAd__TenantId: 'common'`); tenant restriction delegated to an app-level `HomeTenantId` check that cannot be verified from IaC |
| **Suggested fix** | Deploy the License Portal tenant-scoped, or verify that it enforces `HomeTenantId` server-side on every request. |
| **What was tested** | The **hpam-marketplace** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpam-marketplace-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: **no vector can honestly be derived, and that is the finding.** `license/main.bicep:228` sets `AzureAd__TenantId` to `'common'` and `:232` adds a separate `HomeTenantId` setting. The whole severity turns on whether the portal enforces `HomeTenantId` against the token's `tid` claim on every request — **and that code is not in this repository; it is the zip fetched from the blob in `DELTA-MK-01`.** If enforced, this is Informational hardening; if not, any Microsoft work or school account in any tenant can sign in to the licence admin portal, which is a High. **Three bands apart, and nothing here chooses between them. Inventing a midpoint is exactly the "unverified number wearing better clothes" this round exists to stop — the `[GAP]` is preserved deliberately.** **`MK-01` and `MK-04` are blocked on the same missing artefact: getting the License Portal source is ONE commission that closes TWO rows, and it needs no tenant and no live access.**]* |
| **How to resolve** | Deploy tenant-scoped (`AzureAd__TenantId = <tenantId>`), or verify the portal enforces `HomeTenantId` server-side on every request. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpam-marketplace-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### DELTA-MK-05 — SignalR upstream `auth: { type: 'None' }` and deploymentScripts run with `--debug` (Low / Informational)

| Finding `DELTA-MK-05` | **Low** · CVSS 3.1 **(a) Informational · (b) 4.3** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` · component **hpam-marketplace** |
|---|---|
| **The issue** | SignalR upstream `auth: { type: 'None' }` and deploymentScripts run with `--debug` |
| **Suggested fix** | Give the SignalR upstream a real authentication scheme in place of `type: 'None'`, and remove `--debug` from the deployment scripts. |
| **What was tested** | The **hpam-marketplace** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpam-marketplace-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed-with-wording. **(a) the SignalR `auth: { type: 'None' }` upstream is blocked by a control declared 70 lines further down the same file and the finding does not mention it** — `bicep/main.bicep:250-251` sets Easy Auth v2 `requireAuthentication: true` / `unauthenticatedClientAction: 'Return401'` with an `allowedApplications` pin, so an unauthenticated forger is rejected with 401. The residual is a genuine hardening gap that would matter the moment Easy Auth is relaxed, but **its impact today is Informational, `C:N/I:N/A:N`.** **And that mitigation raises a question the finding did not ask: if Easy Auth returns 401 to unauthenticated callers and SignalR calls the upstream with no authentication, the callback should never succeed — so either there is an exclusion nobody has found, or the feature is non-functional as deployed. Named, not filed; both answers matter.** (b) `az --debug` on both deploymentScripts stands as filed at 4.3.]* |
| **How to resolve** | Replace the SignalR upstream's `auth: { type: 'None' }` with a managed identity or a key-based scheme, and remove `--debug` from the `deploymentScripts` invocations so deployment logs stop carrying diagnostic detail. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-01 — Unauthenticated, implicitly-exported runtime broadcast receivers let any co-located app emulate a card tap and force sign-in / sign-out (bypasses the card reader and the token-service signature gate entirely)

| Finding `D-01` | **Critical** · CVSS 3.1 **9.2** `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` · component **HPAuthenticationManager** |
|---|---|
| **The issue** | Unauthenticated, implicitly-exported runtime broadcast receivers let any co-located app emulate a card tap and force sign-in / sign-out (bypasses the card reader and the token-service signature gate entirely) |
| **Suggested fix** | Delete the test receiver from release builds, register the sign-in and sign-out receivers with `RECEIVER_NOT_EXPORTED`, and set an explicit `targetSdk` of 34 or above so unflagged registrations fail the build. |
| **What was tested** | The **HPAuthenticationManager** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpauthenticationmanager-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[HIGH 8.7 to CRITICAL 9.2, 2026-09-09. The vector holds at source; the filed number simply was not what it produces — and the `[ASSUMPTION]` this finding rested on is now a MEASUREMENT.** Exploitability depended on `targetSdk < 34`, which the reviewer could only assume. Resolved: `targetSdk` is **absent from `app/build.gradle.kts`, absent from both `AndroidManifest.xml` files (no `<uses-sdk>` element at all), and returns zero hits anywhere in the tree**, while `minSdk` is **31**. With `targetSdkVersion` absent the platform defaults it to `minSdkVersion` = 31, and Android 14's mandatory receiver-export flag applies only to apps targeting 34+. **The unflagged registrations are exported by default, reachable by any app on the device, and do not throw.** **One reviewer control is off by one and the conclusion is unaffected:** there is exactly **one** flagged `registerReceiver` call, not two (`DefaultConfigProvider.kt:95` does not reproduce), and **four** registration sites, not five (the reviewer's fifth is an `unregisterReceiver(` their substring grep also matched). The control still fires — the project knows the flag API and uses it once. **THE `UI` CALL IS SETTLED AT SOURCE, 2026-09-09, AND IT IS SETTLED FOR THIS ROW AND JUNE `F-07` TOGETHER — `UI:N` STANDS, SO 9.2 CRITICAL STANDS. §2.3.7 open item 3 IS CLOSED.** The trigger was read rather than reasoned about: `PrinterAuthenticationService.kt:58-66` registers both receivers with the two-argument `registerReceiver(receiver, filter)` — **no `RECEIVER_NOT_EXPORTED` flag and no broadcast permission** — on `IntentFilter(packageName + ".signin")` and `".signout"`, and `onReceive` calls `onSignIn(null)` / `onSignOut()` **unconditionally, with no sender check, no permission check and no validation of the intent**. The author's own reproduction command sits in the code as a comment at `:62`: `adb shell am broadcast -a com.hp.print.hpauthenticationmanager.signout`. **A co-located application reaches this surface unaided, with one `sendBroadcast` call. No second person acts, and no card is tapped — removing the human card tap is the whole point of the finding, so `UI:R` would price away the very thing being reported.** CVSS 3.1 §2.1.4 requires a human *other than the attacker* to participate; nobody does. **And getting the attacker's code onto the device is already priced into `AV:L` — charging it again in `UI` is the same double-count this register has now ruled an error twice** (`H-D1`'s `S:C`/`AV:N`, `ADM-D4`'s `PR:H` against `AC:H`). **What the device question actually governs, stated so it is not lost:** whether a locked Workpath kiosk permits third-party installation at all is a real and unanswered question, but it is an **environmental** one — it bears on `MAV`/likelihood, not on a base metric. **The base is settled statically; the environmental score is not, and needs a device.**] |
| **How to resolve** | Delete the `"action"` receiver from release builds (guard with `BuildConfig.DEBUG && isEmulator()`, or move to an `androidTest` helper). Register `.signin`/`.signout` with `ContextCompat.RECEIVER_NOT_EXPORTED`, or drop them — `PrinterAuthenticationService` already receives sign-out from the Workpath platform. Set an explicit `targetSdk` (≥ 34) so unflagged registrations fail the build/boot rather than silently export. Add a lint rule failing on `registerReceiver(` without an export flag. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpauthenticationmanager-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-02 — HPCC "Custom" cloud configuration re-points the OAuth authority, Graph and Monitor endpoints with no scheme or host validation; HPAM then re-broadcasts the endpoints to four consumer apps and embeds them in the HPSA provisioning QR

| Finding `D-02` | **High** · CVSS 3.1 **7.9** `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:L` · component **HPAuthenticationManager** |
|---|---|
| **The issue** | HPCC "Custom" cloud configuration re-points the OAuth authority, Graph and Monitor endpoints with no scheme or host validation; HPAM then re-broadcasts the endpoints to four consumer apps and embeds them in the HPSA provisioning QR |
| **Suggested fix** | Require `https://`, reject userinfo, ports and paths, and pin `Custom` hosts to the Microsoft national-cloud allow-list — or remove `Custom` and keep only the five sovereign presets. |
| **What was tested** | The **HPAuthenticationManager** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpauthenticationmanager-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed at source, band unchanged, 7.5 to 7.9. `util/CloudConfigExtensions.kt:5-7` is the whole validation, and **the contrast the finding draws is a genuine internal positive control**: the legacy Keycloak path at `WorkpathConfigProvider.kt:227` *does* `require(config.baseUrl.startsWith("https://"))`. The codebase knows how to demand HTTPS and does not demand it here. **One evidence leg does not hold in this snapshot and it does not change the score:** the listed propagation to four sibling apps via `CloudConfigService` is not reachable, because that service is declared in no manifest (see `D-07`). `S:C` survives on the QR path to the phone, which crosses an authority boundary on its own. **Wording correction, not a re-score.**]* |
| **How to resolve** | Validate `Custom` values: require `https://`, reject userinfo/ports/paths, and pin the host to an allow-list of Microsoft national-cloud endpoints (`login.microsoftonline.{com,us}`, `login.partner.microsoftonline.cn`, `graph.microsoft.{com,us}`, `dod-graph.microsoft.us`, `microsoftgraph.chinacloudapi.cn`, `monitor.azure.{com,us,cn}`) — the five sovereign presets already in `cloudconfig/model/CloudConfig.kt:8-30` are the whole legitimate universe. Alternatively remove `Custom` and keep only the enum. Apply the same allow-list in the QR consumer (CK-01 remediation) and in the four `CloudConfigProxy` consumers so a defect in HPAM cannot be inherited. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpauthenticationmanager-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-03 — The complete HPCC configuration — including the tenant's Entra client secret and API key — is logged at INFO level on every config consume, and INFO-level messages are shipped to Microsoft AppCenter, in release builds, with no debug gesture required

| Finding `D-03` | **High** · CVSS 3.1 8.7 `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` · component **HPAuthenticationManager** |
|---|---|
| **The issue** | The complete HPCC configuration — including the tenant's Entra client secret and API key — is logged at INFO level on every config consume, and INFO-level messages are shipped to Microsoft AppCenter, in release builds, with no debug gesture required |
| **Suggested fix** | Log key names and never values, stop passing free-text messages as AppCenter event names, and treat third-party telemetry as customer-opt-in. |
| **What was tested** | The **HPAuthenticationManager** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpauthenticationmanager-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: **confirmed line for line — vector and number both already exactly right, the cleanest row in the partition. No change.** `Loggable.kt:71-74` (release `logLevel` is `Info`), `:104-111` (`if (level >= Log.INFO) Analytics.trackEvent(message, …)`, so **the whole formatted message string becomes the AppCenter event name**), `WorkpathConfigProvider.kt:189` (`logI { "getRemoteConfig() = $wrapped" }` where `wrapped` is the raw HPCC JSON), and AppCenter starts unconditionally at `App.kt:86-93`.]* |
| **How to resolve** | Log only fidget ids/keys, never values (`WorkpathConfigProvider.kt:187`); or redact with the same purge routine used at `:111-155` before logging. Stop passing free-text messages as AppCenter event names (`Loggable.kt:111`) — send structured, allow-listed event identifiers; treat AppCenter as customer-opt-in. Remove the email/property/cookie/serial `logI` sites listed above. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpauthenticationmanager-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-04 — The token broker hands one union-scoped delegated Graph token to every consumer app, exposes the directory-stored refresh token and card blobs through `getProperty`, and lets consumers create arbitrary searchable CSA definitions

| Finding `D-04` | **Medium *(bucketed)*** · CVSS 3.1 **7.9 base** `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` · component **HPAuthenticationManager** |
|---|---|
| **The issue** | The token broker hands one union-scoped delegated Graph token to every consumer app, exposes the directory-stored refresh token and card blobs through `getProperty`, and lets consumers create arbitrary searchable CSA definitions |
| **Suggested fix** | Issue per-application scoped tokens, allow-list the `getProperty` keys so `refreshToken` and `cardId` cannot be read, and bind callers by package and signing-certificate hash at `onBind`. |
| **What was tested** | The **HPAuthenticationManager** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpauthenticationmanager-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[QUALIFIER RESTORED 2026-09-09 — this was a register transcription defect, not a finding defect.** The delta file's severity line reads, verbatim: *"Medium (CVSS 7.8 base; **bucketed Medium because standalone exploitation requires an already-trusted consumer app** — it becomes High when chained with F-07/F-12)"*. **The register printed a bare "Medium \| 7.8" with the reason removed, which reads as an error and invites a future pass to "fix" it.** Vector holds at source (`PR:H` = an already-trusted, signature-matched consumer app — exactly the stated reason for the bucketing); the number is 7.9, not 7.8. **Band Medium is a deliberate, documented judgement and must not be corrected to match the number.**] |
| **How to resolve** | Issue per-app tokens: have each consumer register the resource scopes it needs and let HPAM perform a refresh-token grant with those scopes (`scope=` on the `refresh_token` grant), or use OBO. Allow-list `getProperty`/`updateProperty` keys (deny `refreshToken`, `cardId`, `@odata*`); never create definitions from consumer input. Bind callers by package allow-list *and* signing-cert hash at `onBind`. Set `isSearchable=false` on `refreshToken`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpauthenticationmanager-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-05 — Additional committed credentials not in F-16's inventory, sitting in the one directory the new gitleaks CI gate is configured to ignore

| Finding `D-05` | **Medium *(bucketed)*** · CVSS 3.1 **8.1 base** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` · component **HPAuthenticationManager** |
|---|---|
| **The issue** | Additional committed credentials not in F-16's inventory, sitting in the one directory the new gitleaks CI gate is configured to ignore |
| **Suggested fix** | Rotate all four credentials, replace the test fixtures with placeholders, delete the gitleaks allow-list that hides the directory, and inject `config.properties` from CI secrets. |
| **What was tested** | The **HPAuthenticationManager** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpauthenticationmanager-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[QUALIFIER RESTORED 2026-09-09, and the base vector was itself wrong.** Verbatim from the delta file: *"Medium (**bucketed Medium because the values are dev-staging tenant material and validity is `[UNVERIFIED]`; joins F-16 Critical if live**)"*. The filed vector asserted `PR:N` — but the exposure is credentials committed to a **private repository**, and reading it requires repository credentials, so `PR:N` (an attacker with no privileges at all, over the internet) is not supportable. **`PR:L`: base 8.1, not the 9.1 printed.** **The escalation condition stays on the row: this joins `F-16` at Critical if the credentials are live — and that is a live check, which is held.**] |
| **How to resolve** | Rotate all four (treat as compromised). Replace the cfg fixtures with placeholder values (the tests already regex-strip `apikey`/`serviceEndpointSecret` — `WorkpathConfigProviderTest.kt:44-45` — so real values are not needed). Delete the allow-list; delete `config.properties` from VCS and inject via CI secrets (`build.gradle.kts:14-18` reads it from `rootDir`). Make the gitleaks job a required check and confirm it fails on a seeded test secret. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpauthenticationmanager-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-06 — The runtime debug toggle also enables OkHttp `Level.BODY` logging on all three HTTP clients, dumping the client secret, all tokens and every Graph CSA response to Logcat

| Finding `D-06` | **Medium** · CVSS 3.1 **5.5** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` · component **HPAuthenticationManager** |
|---|---|
| **The issue** | The runtime debug toggle also enables OkHttp `Level.BODY` logging on all three HTTP clients, dumping the client secret, all tokens and every Graph CSA response to Logcat |
| **Suggested fix** | Never attach a BODY-level interceptor outside `BuildConfig.DEBUG`; if field diagnostics are required use `Level.BASIC` with `redactHeader("Authorization")` and body suppression on the token paths. |
| **What was tested** | The **HPAuthenticationManager** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpauthenticationmanager-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed, 6.2 to 5.5, band unchanged. **The reviewer's own honest limit on their finding is worth keeping and was verified:** the interceptor writes via `logD`, which is **below** the INFO threshold at `Loggable.kt:104`, so the dump stays in Logcat and does **not** reach AppCenter.]* |
| **How to resolve** | Never attach a BODY-level interceptor outside `BuildConfig.DEBUG`; if field diagnostics are required use `Level.BASIC` with header redaction (`redactHeader("Authorization")`) and body suppression for `/oauth2/` and `customSecurityAttributes` paths. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpauthenticationmanager-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-07 — `CloudConfigService.getConfig()` has no caller check while its sibling methods do

| Finding `D-07` | **Informational** · CVSS 3.1 **n/a — no reachable path in this snapshot** · component **HPAuthenticationManager** |
|---|---|
| **The issue** | `CloudConfigService.getConfig()` has no caller check while its sibling methods do |
| **Suggested fix** | Gate `getConfig()` as its sibling methods are gated, or make the service non-exported and bind by explicit component only. |
| **What was tested** | The **HPAuthenticationManager** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpauthenticationmanager-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[LOW 3.3 to INFORMATIONAL, 2026-09-09 — the code defect is real, the reachability is not, and the citation is REFUTED.** The code claim is confirmed: `CloudConfigService.kt:76-78` — `getConfig()` returns the DTO with no `enforceSameSignature()` while `registerCallback` and `unregisterCallback` both call it. **The reachability premise fails three ways:** the cited `AndroidManifest.xml:109-113` is **`PrinterAuthenticationService`**, guarded by `SERVICES_PERMISSION` — not the cited service and not `GET_PACKAGE_SIZE`; `GET_PACKAGE_SIZE` actually guards `TokenManagementService` at `:80-83`; and **`CloudConfigService` is absent from both manifests**, of which there are exactly two in the tree with no build-variant manifest. **Positive control, because "not declared" is an absence:** the app manifest **does** declare four other services, so the project declares services when it intends them to be bindable — the absence is a measurement, not an idiom. An Android `Service` absent from the merged manifest cannot be bound by anyone, and `CloudConfigProxy.kt:122` binds it by explicit component name. **REACHABILITY GATE: if any shipped or merged manifest declares `CloudConfigService`, this row returns to Low 3.3 immediately** — and the missing `enforceSameSignature()` becomes live at that moment. **NOT TESTED: the manifest merger was not run and the two `WorkpathLib` AARs were not decompiled.**] |
| **How to resolve** | Gate `getConfig()` like its siblings, or make the service non-exported and bind by explicit component only. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpauthenticationmanager-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### D-08 — Sign-in attributes passed to the Workpath platform contain a hardcoded password and placeholder external e-mail addresses

| Finding `D-08` | **Low** · CVSS 3.1 — *(correctly unscored; `[UNVERIFIED impact]` tag now RESOLVED)* · component **HPAuthenticationManager** |
|---|---|
| **The issue** | Sign-in attributes passed to the Workpath platform contain a hardcoded password and placeholder external e-mail addresses |
| **Suggested fix** | Remove the placeholder addresses and the hardcoded password, and document the Workpath behaviour the attributes are meant to produce. |
| **What was tested** | The **HPAuthenticationManager** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/hpauthenticationmanager-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: **band unchanged, score still correctly absent — but the open `[UNVERIFIED impact]` tag is closed by measurement, and it closes BOTH WAYS.** The vendor javadoc (`WorkpathLib-javadoc.jar`, expanded **into the session scratchpad**, `Source_Code/` untouched) settles it: `setPassword` is documented as *"user's password (or PIN) **as gathered by the authentication process** … **may be null**"* — so `null` is the sanctioned value when no password was gathered, and HPAM's card-tap flow gathers none and supplies the literal `"password"`. **Confirmed as a fabricated credential.** But `UserOverridesAttributes.Builder` has **no `setTo`, `setCc` or `setBcc`** — so the `bcc1@`/`cc1@`/`to1@` placeholders **cannot reach the platform through this API**, and the BCC/CC exfiltration worry is **REFUTED**. The `From` override is real and confirmed. **The finding is narrower and better evidenced than it was filed.**]* |
| **How to resolve** | Remove placeholder addresses (pass empty overrides); do not supply a password when the platform does not need one; document the intended Workpath behaviour. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/hpauthenticationmanager-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D1 — Marketplace webhook accepts an UNVERIFIED JWT: signature never checked, and the two claim values it compares are a public Microsoft constant and a committed tenant id

| Finding `ADM-D1` | **High** · CVSS 3.1 **7.5** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` · component **datasec-administration-portal** |
|---|---|
| **The issue** | Marketplace webhook accepts an UNVERIFIED JWT: signature never checked, and the two claim values it compares are a public Microsoft constant and a committed tenant id |
| **Suggested fix** | Register a real JWT bearer scheme with issuer, audience, lifetime and signing-key validation, and keep the `appid` comparison only as an additional claim requirement after the signature is checked. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/datasec-administration-portal-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed at source, band holds; **the `A:L` aggravator is REFUTED** — there is no availability impact on this path — so 8.2 to 7.5. Chain re-derived exactly: `WebhooksController.cs:13` `[AllowAnonymous]`, `:78-80` gated only by a code equality test, and `SubscriptionWebhookCommandHandler.cs:50-58` calls **`ReadJwtToken`**, which parses and does not validate. **The reviewer's positive control fires:** signature-validation vocabulary across all `*.cs` returns **zero matches**, positive control `TokenValidationParameters\|JwtSecurityTokenHandler\|JwtBearerOptions` returns **7 hits**. The absence is a measurement. **And `Program.cs:121-125` configures `ValidAudience`/`ValidIssuer` for a scheme that is never registered — dead configuration that reads, to a maintainer, exactly like a control.**]* |
| **How to resolve** | 1. Register a real bearer scheme: `.AddJwtBearer(Constants.Identity.AuthenticationSchemes.BearerSaaS, o => { o.Authority = "https://login.microsoftonline.com/<publisher tenant>/"; o.TokenValidationParameters.ValidAudience = <Marketplace app registration client id>; o.TokenValidationParameters.ValidateIssuer/Lifetime/IssuerSigningKey = true; })` and put `[Authorize(AuthenticationSchemes = BearerSaaS)]` on the webhook action; delete the manual claim comparison (`:50-82`) and the dead `Configure<JwtBearerOptions>` block. 2. Keep the `appid == 20e940b3-…` check as an *additional* claim requirement after signature validation (Microsoft's documented pattern), never as the primary gate. 3. Before mutating state, fetch the operation from the Marketplace Operations API (`GET /saas/subscriptions/{id}/operations/{operationId}`) and act on *that*, not on the posted body. 4. Drop the query-string `code` for this route once bearer auth is in place (query strings land in App Service / App Insights logs). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/datasec-administration-portal-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D2 — `POST /api/saas` (representative create) has no ownership check: any Entra user in any tenant can pre-register the HP representative for any subscription id

| Finding `ADM-D2` | **Medium** · CVSS 3.1 **5.4** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:L` · component **datasec-administration-portal** |
|---|---|
| **The issue** | `POST /api/saas` (representative create) has no ownership check: any Entra user in any tenant can pre-register the HP representative for any subscription id |
| **Suggested fix** | Require the caller's tenant to match the subscription's beneficiary, bind the subscription id server-side from the Marketplace token, and make the ownership test a resource-based authorisation handler rather than a per-handler check. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/datasec-administration-portal-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: **confirmed outright — vector re-derives unchanged.**]* |
| **How to resolve** | 1. In `RepresentativeCreateCommandHandler`, load the subscription, and require `caller.tid == subscription.Beneficiary.TenantId` (or `caller.email == BeneficiaryEmail`) — reject otherwise. Store `CreatedByObjectId`/`CreatedByTenantId` on the representative row. 2. Require the Marketplace landing `token` on the create call too, and bind the resolved subscription id server-side rather than trusting the body. 3. Make `AssignmentToSaaSCustomerPolicy` require a `tid` claim and evaluate ownership in a resource-based `IAuthorizationHandler`, so the check is structural rather than per-handler (charter §4d: prefer a structural guard). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/datasec-administration-portal-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D3a — The provisioned Keycloak realm auto-links federated identities with both first-broker-login verification steps deleted, so an identity provider that asserts an existing user's e-mail address is linked to that account unverified

| Finding `ADM-D3a` | **Medium *(bucketed; base 7.1 recorded and deliberately NOT published as the band)*** · CVSS 3.1 **7.1 base** `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` · component **datasec-administration-portal** |
|---|---|
| **The issue** | The provisioned Keycloak realm auto-links federated identities with **both** first-broker-login verification steps deleted, so an identity provider that asserts an existing user's e-mail address is linked to that account unverified |
| **Suggested fix** | Restore "Confirm link existing account" and "Verify existing account by email", and make the automatic-link execution `ALTERNATIVE` behind that verification. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[SPLIT OUT OF `ADM-D3` ON TUESDAY'S RULING 2026-09-09 — §2.3.7 open item 1d, ACCEPT. This is the dominant sub-item.** Re-derived at source by the finalise seat independently of seat D: `Constants.cs:233` sets `DeleteNames` to *Confirm link existing account* and *Custom First broker Login – auto Merge Account verification options*; `AuthenticationFlowCleanCommandHandler.cs:42` filters the realm's executions by exactly that list and deletes them; `AuthenticationFlowAddCommandHandler.cs:34` then adds an `AddExecutionRequest` whose provider is the hardcoded `"idp-auto-link"` (`AddExecutionRequest.cs:8`). **The verification steps are removed and the auto-link step is added, in that order, by the provisioning code itself.** **`UI:R` to `UI:N` is settled from source and is the one metric the code decides:** auto-link fires during **first broker login — the attacker's own login** — and CVSS 3.1 §2.1.4 requires a human *other than the attacker* to participate. Nobody else acts. `AC:H` correct — it needs a second IdP or an existing local user, or a customer IdP inducible into asserting a chosen address; those are outside the attacker's control. `S:C` correct — the vulnerable component is the portal's provisioning code, the impacted component is the realm and every application that trusts it. **THE BASE IS 7.1 AND IT IS DELIBERATELY NOT PUBLISHED AS THE BAND.** Seat D refused to publish 7.1 for the *bundle* on the ground that one vector cannot describe five defects; **splitting dissolves that objection, and it does not dissolve the other two.** The reviewer's qualifiers — exploitability *Suspected*, reachability reduced by the Keycloak-retirement attestation — survive the split and are what hold this at Medium. **The bucket and the number travel together, exactly as on `ADM-D4`.** **NOT TESTED: whether any realm provisioned before the Keycloak retirement is still live.** That is the reachability gate, it is a live check, and it is held. Also untested: whether the customer IdPs set `email_verified`.] |
| **How to resolve** | Restore the `Confirm link existing account` and `Verify existing account by email` executions, or at minimum require the identity provider's `email_verified` claim, and make the automatic-link execution `ALTERNATIVE` behind that verification. One of five sub-items split out of the parent `ADM-D3`; the Keycloak-retirement qualifier travels with it. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D3b — The provisioned public client `HP-Secure-Authentication` has the OAuth 2.0 implicit flow enabled, so tokens are returned through the front channel to a client that cannot authenticate itself

| Finding `ADM-D3b` | **Medium *(reachability reduced by the Keycloak-retirement attestation; exploitability marked Suspected by the reviewer — both qualifiers survive the split, per seat D)*** · CVSS 3.1 **n/a — configuration weakness; no attack path established from this repository** · component **datasec-administration-portal** |
|---|---|
| **The issue** | The provisioned **public** client `HP-Secure-Authentication` has the OAuth 2.0 **implicit flow** enabled, so tokens are returned through the front channel to a client that cannot authenticate itself |
| **Suggested fix** | Set `implicitFlowEnabled=false` on the public client and enforce PKCE with `pkce.code.challenge.method=S256`. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[SPLIT OUT OF `ADM-D3` 2026-09-09 — §2.3.7 open item 1d, ACCEPT.** `ClientsCreateCommandHandler.cs:51-62` sets `ImplicitFlowEnabled = true` together with `PublicClient = true`. The OAuth 2.0 Security BCP deprecates implicit for precisely this reason, and OAuth 2.1 removes it. **NO CVSS, DELIBERATELY.** No attack path has been established from this repository, and **scoring an architectural baseline that is merely unmet manufactures a High out of the absence of barriers** — `AV:N/AC:L/PR:N/UI:N` with three `Low` impacts computes 7.3 on nothing. This is the convention this register already applies at `I-D9`, `I-D10`, `H-D7`, `H-D8`, `NEW-6` (LicenseServer) and `DELTA-MK-04`, and it is round 2's clearest methodological result. **Static analysis only.**] |
| **How to resolve** | Set `implicitFlowEnabled=false` and enforce PKCE with `pkce.code.challenge.method=S256` on the public `HP-Secure-Authentication` client. One of five sub-items split out of the parent `ADM-D3`; the Keycloak-retirement qualifier travels with it. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D3c — The same public client has direct access grants (the resource-owner password credentials grant) enabled, so end-user passwords are presented directly to a client that holds no secret

| Finding `ADM-D3c` | **Medium *(reachability reduced by the Keycloak-retirement attestation; exploitability marked Suspected by the reviewer — both qualifiers survive the split, per seat D)*** · CVSS 3.1 **n/a — configuration weakness; no attack path established from this repository** · component **datasec-administration-portal** |
|---|---|
| **The issue** | The same public client has **direct access grants** (the resource-owner password credentials grant) enabled, so end-user passwords are presented directly to a client that holds no secret |
| **Suggested fix** | Set `directAccessGrantsEnabled=false`: the resource-owner password grant has no place on a public client. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[SPLIT OUT OF `ADM-D3` 2026-09-09 — §2.3.7 open item 1d, ACCEPT.** `ClientsCreateCommandHandler.cs:51-62` sets `DirectAccessGrantsEnabled = true` with `PublicClient = true`. ROPC defeats MFA and consent by design and is removed in OAuth 2.1. **NO CVSS, DELIBERATELY.** No attack path has been established from this repository, and **scoring an architectural baseline that is merely unmet manufactures a High out of the absence of barriers** — `AV:N/AC:L/PR:N/UI:N` with three `Low` impacts computes 7.3 on nothing. This is the convention this register already applies at `I-D9`, `I-D10`, `H-D7`, `H-D8`, `NEW-6` (LicenseServer) and `DELTA-MK-04`, and it is round 2's clearest methodological result. **Static analysis only.**] |
| **How to resolve** | Set `directAccessGrantsEnabled=false` on the same public client, removing the resource-owner password grant. One of five sub-items split out of the parent `ADM-D3`; the Keycloak-retirement qualifier travels with it. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D3d — The same public client is provisioned with wildcard web origins, so any web origin is permitted to make browser calls on its behalf

| Finding `ADM-D3d` | **Medium *(reachability reduced by the Keycloak-retirement attestation; exploitability marked Suspected by the reviewer — both qualifiers survive the split, per seat D)*** · CVSS 3.1 **n/a — configuration weakness; no attack path established from this repository** · component **datasec-administration-portal** |
|---|---|
| **The issue** | The same public client is provisioned with **wildcard web origins**, so any web origin is permitted to make browser calls on its behalf |
| **Suggested fix** | Limit `webOrigins` to the application's own origins and set explicit post-logout redirect URIs. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[SPLIT OUT OF `ADM-D3` 2026-09-09 — §2.3.7 open item 1d, ACCEPT.** `ClientsCreateCommandHandler.cs:51-62` sets `WebOrigins` to the single-element wildcard array. **NO CVSS, DELIBERATELY.** No attack path has been established from this repository, and **scoring an architectural baseline that is merely unmet manufactures a High out of the absence of barriers** — `AV:N/AC:L/PR:N/UI:N` with three `Low` impacts computes 7.3 on nothing. This is the convention this register already applies at `I-D9`, `I-D10`, `H-D7`, `H-D8`, `NEW-6` (LicenseServer) and `DELTA-MK-04`, and it is round 2's clearest methodological result. **Static analysis only.**] |
| **How to resolve** | Replace the wildcard `webOrigins` with the application's own origins, and set explicit `post.logout.redirect.uris`. One of five sub-items split out of the parent `ADM-D3`; the Keycloak-retirement qualifier travels with it. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D3e — Every provisioned realm is created with an SSO session idle timeout and maximum lifespan of exactly 180 days, neither settable per realm

| Finding `ADM-D3e` | **Low *(reachability reduced by the Keycloak-retirement attestation; exploitability marked Suspected by the reviewer — both qualifiers survive the split, per seat D)*** · CVSS 3.1 **n/a — a session-lifetime posture, not an attack path** · component **datasec-administration-portal** |
|---|---|
| **The issue** | **Every** provisioned realm is created with an SSO session idle timeout **and** maximum lifespan of exactly **180 days**, neither settable per realm |
| **Suggested fix** | Reduce the SSO idle and maximum session lifetimes from months to hours, and enable brute-force protection in `CreateRealmRequest`. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[SPLIT OUT OF `ADM-D3` 2026-09-09 — §2.3.7 open item 1d, ACCEPT.** `CreateRealmRequest.cs:14,17` — `SsoSessionIdleTimeout` and `SsoSessionMaxLifespan` are both the hardcoded literal `15552000` seconds, and 15552000 ÷ 86400 = **exactly 180**. Both are get-only properties on the record, so no caller can override them. **NO CVSS, DELIBERATELY, and for a second reason beyond the convention above: this sub-item has no attacker of its own.** It does not create a path; it lengthens the window on every other path, which is why bundling it under one vector with the auto-link defect was never going to work. **Static analysis only.**] |
| **How to resolve** | Set the realm's SSO idle and maximum session lifetimes to hours rather than 180 days, and enable brute-force protection in `CreateRealmRequest`. One of five sub-items split out of the parent `ADM-D3`; the Keycloak-retirement qualifier travels with it. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D3 — The Keycloak realm the portal provisions has a weak trust posture: unverified automatic account-linking, a public client with implicit + password grants and wildcard web-origins, 180-day SSO sessions, and a confidential client left on `redirectUris [""]`

| Finding `ADM-D3` | **SPLIT 2026-09-09 — superseded by `ADM-D3a` … `ADM-D3e`** · CVSS 3.1 *(see the five rows above)* · component **datasec-administration-portal** |
|---|---|
| **The issue** | **ROW RETAINED, NOT DELETED, AND NOT COUNTED — it is the parent of the five rows above, kept so the split is auditable.** **THE SIXTH SUB-ITEM, RECORDED HERE RATHER THAN FILED, BECAUSE IT IS MEASURED INERT.** The original row also named *a confidential client left on `redirectUris ["*"]`*. That wildcard is the record default (`CreateClientRequest.cs:20`) and it lands on **only** the confidential client `HP-Authentication-Manager`, which `ClientsCreateCommandHandler.cs:34-40` creates **without** setting either browser flow — so `StandardFlowEnabled` and `ImplicitFlowEnabled` are **both false** and no redirect flow ever consults the URI list. **The public client, which does run browser flows, overrides the default with a single concrete custom-scheme URI (`:60`) and does not carry the wildcard at all.** **So the register's five counted rows plus this measured-inert sixth account for the whole of the original bundle: nothing has been dropped.** *(Seat D reached the same conclusion on `standardFlowEnabled` alone; the second flow flag makes it stronger.)* **Also observed while re-deriving, NOT filed, and named so it is not lost:** `CreateClientRequest.cs:40` hardcodes `FullScopeAllowed = true` as a get-only default on **every** client this portal provisions, which places all realm roles in every issued token. That is a seventh weakness in the same bundle, no seat scoped it, and the finalise seat is not authorised to raise findings on its own initiative. **It needs an owner.** **Original row text and evidence, preserved verbatim:** The Keycloak realm the portal provisions has a weak trust posture: unverified automatic account-linking, a public client with implicit + password grants and wildcard web-origins, 180-day SSO sessions, and a confidential client left on `redirectUris ["*"]` |
| **Suggested fix** | Superseded by the five rows above; the fixes are recorded on `ADM-D3a` to `ADM-D3e`. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. The claim under test: *The Keycloak realm the portal provisions has a weak trust posture: unverified automatic account-linking, a public client with implicit + password grants and wildcard web-origins, 180-day SSO sessions, and a confidential client left on `redirectUris ["*"]`*. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/datasec-administration-portal-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[2026-09-09: confirmed as configuration — all five sub-items re-derived exactly — but the row SHOULD BE SPLIT rather than re-scored, and the arithmetic is corrected without moving the band.** The row recorded 6.2; its own vector produces **6.5**. Both are Medium. **One metric is refutable from source — `UI:R` to `UI:N`**, because the dominant sub-item (`idp-auto-link` with both verification executions deleted) fires during **first broker login, the attacker's own login**; no second person acts. **That would give 7.1 — a High — and the verifier explicitly declines to publish it and recommends nobody else does.** Reason: **this row bundles five distinct configuration weaknesses** (unverified auto-linking, implicit flow, ROPC, wildcard CORS `WebOrigins = ["*"]`, wildcard `RedirectUris = ["*"]`, 180-day SSO sessions) **under one vector, and one vector cannot describe five defects with different attackers and different impacts** — while the reviewer additionally marked the row *exploitability Suspected* and reachability reduced by the Keycloak-retirement attestation. **Turning a Suspected, reachability-reduced bundle into a High by moving one metric is precisely "replacing an unverified number with a differently unverified number".** *(`AC:H` and `S:C` are both confirmed correct. The wildcard-redirect sub-item is already inert — `standardFlowEnabled` is left `false` by the record default — which is itself an argument that these five do not share a band.)* **Splitting creates findings; held for Tuesday, §2.3.7 open item 1.**] |
| **How to resolve** | 1. Restore "Confirm link existing account" / "Verify existing account by email" (or at least require the IdP's `email_verified`), and make the auto-link execution `ALTERNATIVE` behind verification. 2. Public client: `implicitFlowEnabled=false`, `directAccessGrantsEnabled=false`, enforce PKCE (`pkce.code.challenge.method=S256`), `webOrigins` limited to the app's origins, explicit `post.logout.redirect.uris`. 3. Confidential client: set `RedirectUris` explicitly (not `*`) and `fullScopeAllowed=false` with explicit scopes. 4. Realm: SSO idle/max to hours, not months; enable brute-force protection in `CreateRealmRequest`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/datasec-administration-portal-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D4 — Front-end lockfile is deliberately git-ignored and CI `npm install`s unpinned ranges straight into the production artefact; the "Build, Test and Deploy" workflow has no test step

| Finding `ADM-D4` | **Low *(bucketed "environmentally Low")*** · CVSS 3.1 **8.1 base** `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` · component **datasec-administration-portal** |
|---|---|
| **The issue** | Front-end lockfile is deliberately git-ignored and CI `npm install`s unpinned ranges straight into the production artefact; the "Build, Test and Deploy" workflow has no test step |
| **Suggested fix** | Commit `package-lock.json` and remove the ignore rule, switch CI to `npm ci`, pin actions to commit SHAs, and add a test and SCA gate before `deploy_dev`. |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/datasec-administration-portal-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[2026-09-09: confirmed; arithmetic corrected; one metric is a DOUBLE-COUNT; the bucket is PRESERVED.** The row recorded 6.5 and its own vector gives 7.2. **`PR:H` is a double-count** — the attacker needs **no privilege on this system at all**; they need publish rights on some package in the transitive tree, which is an environmental precondition **already** recorded by `AC:H`. Putting it in `PR` as well counts one barrier twice — **the same error round 1 found in `H-D1`, running in the opposite direction (there it inflated; here it deflates).** With `PR:N` the base is **8.1**. **Control fires:** lockfiles to **0**, positive control `package.json` to **1**; all nine runtime dependencies are caret ranges; CI runs `npm install` (not `npm ci`) with **`permissions: write-all`** and an unpinned `@master` action, and there is **no test step** in a workflow named "Build, **Test** and Deploy". **The "environmentally Low" bucket is a judgement and is preserved — but the bucket and the number must travel together.** *(The verifier deliberately did **not** re-derive the impact triad `C:L/I:H/A:L`: those describe a hypothetical malicious payload that no line of the repository determines, and substituting one guess for another was declined. Boundary made visible rather than hidden.)*] |
| **How to resolve** | Commit `package-lock.json`, remove the ignore rule, switch CI to `npm ci`, pin actions to SHAs, add `dotnet test` (and a test project) plus `npm audit --audit-level=high`/SCA as a gate before `deploy_dev`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/datasec-administration-portal-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### ADM-D5 — Event Grid validation handshake and delivery-report ingestion trust the body once the (committed) code is presented

| Finding `ADM-D5` | **Medium** · CVSS 3.1 **5.3** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N` · component **datasec-administration-portal** |
|---|---|
| **The issue** | Event Grid validation handshake and delivery-report ingestion trust the body once the (committed) code is presented |
| **Suggested fix** | Verify the Event Grid handshake and the delivery reports against a secret held outside the repository, rotate the committed code, and authenticate the ingestion endpoint. **This fix is conditional on `INFRA-02`, which is not closed — see §6.2, ruling 1f.** |
| **What was tested** | The **datasec-administration-portal** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/datasec-administration-portal-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** **[2026-09-09: the defect is confirmed exactly at source — `EmailDeliveryEventsProcessingCommandHandler.cs:43-51` echoes `subscription.ValidationCode` straight back, so the holder of the webhook code can point this endpoint at **their own** Event Grid topic, and `:33-41` stores any posted delivery report with **no check of `aeg-event-type` and no check that `gridEvent.Topic` is the expected ACS resource.** **The band and the number contradict each other and NOTHING explains why.** This is the class round 1 catalogued — with one crucial difference: `D-04` and `D-05`'s contradictions were **deliberate and documented**, and `ADM-D5` **carries no qualifier anywhere**; the verifier looked for one. **Exactly one of two things is true and the verifier explicitly referred the choice to Tuesday rather than guess:** either the row is a Medium and the `Low` is a slip, **or** a bucketing reason exists that was never written down and must be written down now. **It also depends on a cross-component premise no seat's partition contained** — `PR:N`/`AC:L` presume the webhook `code` is obtainable, and it is not committed in this repository *(all eleven sensitive settings there are the identical placeholder token — verified structurally, no values read)*; the premise is **INFRA-02 in `infra-administration-portal-main`**. If INFRA-02 holds, `AC:L` to **5.3 Medium**; if it does not, `AC:H` to **3.7 Low**, *and the filed `Low` would then be correct for a reason nobody wrote down.* **RESOLVED 2026-09-09 ON TUESDAY'S RULING — §2.3.7 open item 1f, ACCEPT: Low to MEDIUM 5.3.** The row now says what its own vector says, and the contradiction is closed in the only direction that does not invent a justification: **there was no bucketing reason, because the verifier looked for one in the delta file and in this register and found none.** **The INFRA-02 dependency is NOT closed by this ruling and must not be read as closed.** `AC:L` still presumes the webhook `code` is obtainable, and that premise lives in `infra-administration-portal-main`, which no seat's partition contained. **If INFRA-02 does not hold, `AC:H` gives 3.7 and this row returns to Low** — at which point the original `Low` turns out to have been right for a reason nobody wrote down, and **the reason must then be written down rather than the band merely restored.** One question to whoever owns that repository settles this row and `ADM-D1` together. **Static analysis only; no live pass.**]** |
| **How to resolve** | Validate the Event Grid subscription-validation handshake and the delivery-report ingestion against a secret held outside the repository — or move to the Entra-authenticated webhook delivery Event Grid supports — rotate the committed code, and authenticate the ingestion endpoint. **The band rests on `INFRA-02`:** if that dependency does not hold, this row's vector gives 3.7 and it returns to Low, and the reason must then be written on the row rather than the band merely restored (§6.2, ruling 1f). |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### QA-D1 — Library fetches a host-supplied thumbnail URL with no scheme/host constraint (June lead, still unscored)

| Finding `QA-D1` | **Low** · CVSS 3.1 **3.1** `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N` · component **QuickAccessLibrary** |
|---|---|
| **The issue** | Library fetches a host-supplied thumbnail URL with no scheme/host constraint (June lead, still unscored) |
| **Suggested fix** | Require `https` and an optional consumer-supplied host allow-list at `newInstance(...)`, and cap the fetched image size. |
| **What was tested** | The **QuickAccessLibrary** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/quickaccesslibrary-master.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: **confirmed exactly, and narrowed.** `QuickAccessViewHolder.kt:67-68` loads a host-supplied URL with no scheme check, no host allow-list and no `resize()`; `QAFileItem.kt:11` is mutable and host-populated; the library manifest is **literally empty** (`<manifest></manifest>`) — no `networkSecurityConfig`, no cleartext policy. Census: zero occurrences of `https\|allow\|scheme\|host` anywhere in `quickaccesslib/src/main/java`. **NARROWED: the finding's open worry was that a consumer might not set a cleartext policy — CypherSharePoint, MailFlow and UniversalPrint are all consumers and all three set `usesCleartextTraffic="false"`, so the cleartext leg is closed for every consumer checked.** What remains and is real: an unconstrained HTTPS GET from the MFP to a host-supplied origin — beacon and SSRF-lite. *(Consumers outside that set were not checked.)*]* |
| **How to resolve** | Enforce `https` and an optional host allow-list supplied by the consumer at `newInstance(...)`; cap image size (`resize()`); document that the consumer must set `usesCleartextTraffic=false` or a `networkSecurityConfig`. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/quickaccesslibrary-master.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### QA-D2 — Informational: dependency currency of the only network-capable component

| Finding `QA-D2` | **Info** · no CVSS score recorded · component **QuickAccessLibrary** |
|---|---|
| **The issue** | dependency currency of the only network-capable component. |
| **Suggested fix** | Pin the network stack and put the component under software-composition analysis in CI, so dependency currency is measured rather than assumed. |
| **What was tested** | The **QuickAccessLibrary** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/quickaccesslibrary-master.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed exactly (`quickaccesslib/build.gradle.kts:89` — `picasso:2.8`). **Correctly carries no CVSS.**]* |
| **How to resolve** | Pin the library's network stack to exact versions, add software-composition analysis to CI for this component, and record the result, so that currency is a measurement rather than an assumption. This is the only network-capable component in its group, which is why it is called out. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### WP-D1 — The repository is a secret-bearing archive in a format its own secret-scanning CI cannot inspect

| Finding `WP-D1` | **Low *(bucketed "env-adjusted")*** · CVSS 3.1 **5.3** `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N` · component **WorkPathApplications** |
|---|---|
| **The issue** | The repository is a secret-bearing archive in a format its own secret-scanning CI cannot inspect |
| **Suggested fix** | Keep the offline archive out of the git repository and in an access-controlled artefact store; scan and purge the restored trees before archiving, and rotate the secrets regardless. |
| **What was tested** | The **WorkPathApplications** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/workpathapplicationsandlibrariessources-master.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed; **the filed 5.3 reproduces exactly and the bucket is correct, stated and preserved** (*"env-adjusted to Low because reachability is 'whoever can read the repo'"* — `PR:L` already carries that reachability, and the bucket then discounts it again for an organisationally-controlled population). **The "structurally blind control" claim is now a measurement:** `restore\|bundle\|clone\|unbundle` across `gitleaks.yml` returns **0 matches — there is no restore step**, so the one control added since June scans 661 MB of opaque packfiles plus four small text files. **One factual correction in a deliverable: the delta file says "23 bundles totalling ≈800 MB"; measured, `du -sh bundles/` = 661 MB.** The count of 23 is right; the size was overstated by about a fifth. **LARGEST UNTESTED AREA IN THIS SECTION, stated plainly: no bundle was extracted, cloned or inspected** — headers and `git bundle list-heads` only — so every June statement about SecureAccess, OnGuard and AppAttestation is **neither re-verified nor contradicted**, and the row's "Confirmed (structure) / **Suspected** (secret content)" split is exactly right and must be kept. **Extracting 23 repositories and ~600 branches is an engagement-sized task that needs no live access and no tenant.**]* |
| **How to resolve** | (1) Do not store git bundles in a git repository; if an offline archive is required, keep it in an access-controlled artefact store, encrypted at rest, with an audit trail. (2) Before archiving, run gitleaks/trufflehog against each *restored* repo and purge history (git filter-repo) of the F-12/F-14/F-16 material; rotate the secrets regardless. (3) If the bundles stay, make the CI restore them to a temp dir and scan the restored trees, so the control measures what it claims to. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/workpathapplicationsandlibrariessources-master.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### WP-D2 — Informational: `restore_from_bundles.sh` chunked-bundle path uses an undeclared associative array

| Finding `WP-D2` | **Info** · no CVSS score recorded · component **WorkPathApplications** |
|---|---|
| **The issue** | `restore_from_bundles.sh` chunked-bundle path uses an undeclared associative array. |
| **Suggested fix** | Declare the associative array before use — the chunked-bundle restore path cannot work as written, and it must be fixed before the bundle is relied on to close `WP-D1`. |
| **What was tested** | The **WorkPathApplications** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/workpathapplicationsandlibrariessources-master.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed; **control fires** — `declare -A\|typeset -A` to exit 1, widened to bare `declare` to **the word never appears in the file**, positive control `local` returns **11 hits**; and `#!/bin/bash` on macOS is bash 3.2, which has **no associative arrays at all**, so the string subscript degrades to arithmetic `0`. **Correctly Informational — no attacker — but its real cost is to EVIDENCE, not to security:** this is the code path that restores **SecureAccess**, and a silent skip there means the archive quietly fails to reproduce the security heart of the suite. **Fix this script before anyone relies on it for the `WP-D1` extraction.**]* |
| **How to resolve** | Add the missing `declare -A` for the associative array in `restore_from_bundles.sh`. **This is a prerequisite, not a cosmetic fix:** `WP-D1`'s remediation depends on restoring the bundles and scanning the restored trees, and the chunked-bundle path cannot run as written. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### WP-D3 — Informational: workflow pinning

| Finding `WP-D3` | **Info** · no CVSS score recorded · component **WorkPathApplications** |
|---|---|
| **The issue** | workflow pinning. |
| **Suggested fix** | Pin the workflow's actions to commit SHAs and to major versions that exist. |
| **What was tested** | The **WorkPathApplications** component, as provided in the source snapshot. The claim under test: *Informational: workflow pinning*. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/workpathapplicationsandlibrariessources-master.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was independently re-derived at source in round 2 by a reviewer who did not write it and was instructed to falsify it. Negative claims require a positive control demonstrating that the same instrument, at the same scope, finds the thing when it is present. **Test record.** *[2026-09-09: confirmed exactly (`gitleaks.yml:18` `actions/checkout@v7`, `:23` `gitleaks-action@v3`). Correctly Informational — the workflow's `permissions` are least-privilege, which bounds what a hijacked tag could do here. **Observation worth carrying: the same pattern is in all five components reviewed that day, so this is an estate-wide CI hygiene item and five Informational rows are a poor way to carry one estate-wide fact.**]* |
| **How to resolve** | Pin the workflow's actions to commit SHAs and to major versions that exist. This repository carries the same non-existent `actions/checkout@v7` pin as `I-D9` and `H-D7`, which is why §3.3.1 records the estate-wide claim as understated. |

**Tally for this register's share of this section: 1 Critical, 4 High, 15 Medium, 7 Low and 4
Informational, totalling 31 counted.** **Plus four retained, uncounted rows.** Two are marked
withdrawals, `DELTA-HP-01` and `DELTA-HP-02`, and two are split parents kept so that the split is
auditable, `DELTA-MK-03` and `ADM-D3`, each pointing at the rows that replaced it and each still
carrying its original text and evidence. **Nothing was deleted anywhere in this section.**

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.8 Commercial and product-claim observations

These are recorded because they are product-claim questions before they are security questions. They
are not severity-scored and are not counted in any tally. Each is stated as the issue first and the
suggested action second, with the supporting measurement below it.

**1. `pdf-api`'s infrastructure is not deployed.**

| | |
|---|---|
| **The issue** | All seven module instantiations carry `count = 0`, so every control the module declares — Easy Auth, TLS 1.2, HTTPS-only — is switched-off code. Any running instance is unmanaged drift. |
| **Suggested action** | Establish whether any `pdf-api` instance is running outside Terraform. If one is, its configuration is unknown and unmanaged; if none is, say so, rather than crediting controls that the module declares but does not deploy. |

**2. Two products are called CypherKey.**

| | |
|---|---|
| **The issue** | The folder named `CypherKey` is HPSA, while the folder named `OneTimePad` is CypherKey. A finding labelled "CypherKey" is ambiguous between two authentication products, and the plain-language reading is the wrong one. See the note in §2.3. |
| **Suggested action** | Rename the folders to match the products, and until that is done require every finding, ticket and report to name the product identity rather than the folder name. |

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4. Assurance Observations

Several design elements hold up under review. They are recorded so that the register is not
discounted wholesale, and they do **not** offset the Critical and High findings; they indicate that
the architecture's intent is recoverable once the implementation defects are fixed.

- **The primary Entra authentication path is sound in design.** It is built on OIDC and OAuth2 with
PKCE and delegates identity, MFA and Conditional Access to Microsoft Entra, an out-of-scope,
 vendor-assured platform. The weaknesses are in how the suite *uses* it, most notably the explicit
 no-MFA mode at F-02.
- **No code path was found in the reviewed on-device or HPAM source that captures, proxies or stores
 the user's Entra password.** Authentication is delegated to MSAL and Entra.
- **The documented SignalR design includes replay protection** on the HPAM-to-Entra path. The
 anonymous-broadcast weakness is specific to the cc-api cardless hub at F-06, not to the entire
SignalR design.
- **HP-AuthSuite-Manager is clean on several axes that matter.** Every SQL statement across thirteen
 repositories is fully parameterised; no credential reaches any log, with every logging call
 enumerated including error paths; there is zero committed key material; and there is no identity
 provider of any kind, so it attests Keycloak-clean without qualification.
- **OXPd1 shows deliberate cryptographic discipline** — PBKDF2-HMAC-SHA256 at 65,536 iterations,
 every SQL statement a bound prepared statement, correct PKCE, and deliberate secret redaction. **Its
README understates its own security:** it claims that card sequences are authorised without
 validation, the code does not do that, and the claim should not be quoted as evidence of a weak
 design.
- **Sensitive values such as Card UIDs and customer OIDC secrets are encrypted at rest** rather than
 stored fully in cleartext. An attempt at protection exists, though the algorithm is weak and is
 itself a finding at F-23.

**One credit previously given is withdrawn, and it was customer-facing balance text.** UniversalPrint
was credited with adding real WebView hardening since June, specifically origin pinning and correct
SSL-error cancellation. **All three clauses are wrong.** "Origin pinning": the file is unwired, and
`configureHardenedAuthWebView` returns exactly one occurrence tree-wide, its own definition. "Correct
SSL-error cancellation": `onReceivedSslError` appears zero times in `UniversalPrint-main/app/src`, and
the behaviour is safe only because the Android platform default cancels, which is not something this
team wrote and is not evidence of improvement. "The same file enables WebView debugging
unconditionally": true of the file, false of the application. **A credit granted on unwired code is
worse than no credit, because it is the kind of sentence a customer's own reviewer tests first.**

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 5. Keycloak Retirement Position

The position is now measurable across the components in this register.

| Component | Keycloak references |
|---|---|
| HP-AuthSuite-Manager · pdf-api | **0** |
| OXPd1 | 1 — an explicit comment: *"Keycloak support intentionally omitted"* |
| infra-administration-portal | 2 — a Log Analytics workspace **name** only; no Keycloak provisioned |
| **HPSA** | **10 files / 35 hits — CANNOT be attested clean** |
| datasec-administration-portal (157) · cc-api (50) · HPAM (23) · infra_hpam (17) | unchanged from June |

**The blocking item is HPSA.** In code, Keycloak is the `else` branch of both `auth_module.dart` and
`session_interceptor.dart` — the default whenever `clientId` or `tenantId` is absent — and its QR
payload is the unencrypted one. `token_api.dart:11` hardcodes a production Keycloak host and the
`datasec` realm. This conflicts with the whitepaper's "Appendix A, Legacy Mode" framing.

For the deployment position, see §3.3.2: the infrastructure module is live in all four production
regions, and the code-retirement half of `04_Keycloak_Retirement_Attestation` cannot be attested.

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 6. Verification Status and Open Items

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 6.1 The per-component verification pass

An independent verifier ran per component — **none of them the finder** — each instructed to try to
falsify every finding at source, with five verdicts (confirmed, refuted, downgraded, upgraded,
unverifiable) and a positive control required for every negative claim. All reports are written and
have been read. The table below covers this register's share of that pass.

| Component | CONF | REF | DOWN | UP | UNVERIF | new |
|---|---|---|---|---|---|---|
| HPSA | 16 | 0 | 2 | — | — | 5 |
| HP-AuthSuite-Manager | 12 | 0 | — | 1 | 1 | 2 |
| OXPd1 | 10 | 0 | 3 | — | — | — |
| pdf-api | 9 | 0 | — | — | 1 | — |
| infra-administration-portal | 6 | 0 | 1 | 1 | 1 | 6 |
| **TOTAL** | **53** | — | **6** | **2** | **3** | **13** |

**Not one finding was refuted.** Across the full pass, 149 findings were re-derived at source by
someone who did not write them and was told to break them, and **none collapsed.** Twelve were
over-scored and were corrected downward; five were under-scored; three cannot be settled without a
live system. **The register is conservative, not inflated.**

**This pass covers the findings from the re-run's deep reviews of the actively reviewed new
components. It does not cover the delta findings of §3.4 to §3.7**, which were raised after it ran and
have their own, differently shaped verification recorded on each of those sections. The word
"complete" here means complete over the findings it re-derived, and nothing wider.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 6.1.1 Movements in the Critical count

| Movement | Finding | Basis |
|---|---|---|
| **OUT** | **CK-01 / HPSA** (Critical 9.3 to **High 8.2**) | Vector only: the payload arrives by camera + user action, so CVSS 3.1 §2.1.1 makes it `AV:L/UI:R`, not `AV:N`. **The mechanism is CONFIRMED and is STRONGER than the finder stated.** *(Wednesday's ruling: accept 8.2 as spec-correct, and the register carries this note — its practical deliverability is undiminished, since the delivery vector is a sticker on a printer console. Do not let the bucket change drive prioritisation.)* |
| **IN** | **INFRA-03** (High 7.5 to **Critical ~9.3**) | The verifier read the cipher and the columns: **AES-ECB** — no IV, no authentication, deterministic, raw-UTF-8 key with no KDF — over **customer tenants' Entra app-registration credentials**. A customer-credential vault whose master key is committed. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 6.1.2 Where verification made findings worse

- **INFRA-02** — the verifier read the two handlers the finder had skipped. `onboarding-cleanup`
 irreversibly null-writes the client identifier, client secret and OpenID URL on **every** row older
 than seven days, with no soft delete and no audit trail; `saas-refresh` lets an anonymous caller
 trigger outbound customer email. **No compensating control exists at any layer**, proven three
 ways: `[AllowAnonymous]` appears exactly once across 498 `.cs` files, the application's global
 default is authenticated, and all twelve other controllers carry a real policy.
- **HP-AuthSuite F-01** — the hardcoded printer administrator password is a Datasec cross-product
 default, identical by digest across four components and five files, and it is **sent** to devices
 rather than probed for.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 6.1.3 Corrections to the coordinating reviewer's own figures

- The stated twenty-three-key inventory of `production.tfvar` **is in fact thirty-three**, with
 thirty-one each in dev and staging. The instrument excluded values shorter than fifteen characters:
 a floor was presented as a count.
- This is the same failure as several findings in this register — an instrument whose scope did not
 match the question.

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 6.1.4 Items that remain unverifiable without a live system

Two items in this register cannot be settled statically, and each carries its exact live check.
`PDF-02`, the Gotenberg server-side request forgery, needs the upstream default, and there is no
network access here. `INFRA-05`, whether `azurerm` 3.84.0 marks `app_settings` as sensitive, needs
the provider schema read, or one `terraform plan` in a throwaway environment. A third, `F-08`,
requires the `Wmhelp.XPath2` 1.1.5 function table: whether `fn:doc` is present and whether it
resolves URIs.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 6.2 Round-2 consolidation: what was applied

The round-2 consolidation applied what five verifiers proposed for their own partitions and nothing
else. Five categories were withheld by rule rather than by disagreement: anything a reviewer marked
out of partition; anything two reviewers disagreed on; anything that would create or delete a finding
rather than re-score one; and anything a reviewer flagged as needing a second reader, a live datum, or
the client's decision.

Six proposals were subsequently ruled and all six were accepted and applied. **All six concern
findings in this register.** Two were ruled as **marked withdrawals**, which is not a deletion: the
row stays in the register, marked withdrawn, carrying the measurement that refuted it, and comes out
of the counted total and the severity tallies only. The two split parents are retained on the same
principle.

| # | Proposal | Seat | RULING | Applied as |
|---|---|---|---|---|
| 1a | **Withdraw `D-MF-01`** (MailFlow High 7.5) — premise absent from the component; the evidence appears to be `D-SP-01`'s, transposed | C | **ACCEPT — MARKED WITHDRAWAL** | Row retained and marked **WITHDRAWN**, evidence intact, de-counted. Highs −1. **`D-SP-01`, the row the evidence actually belongs to, is unaffected and still stands.** |
| 1b | **File a new UniversalPrint row** — the three auth WebViews have **no** origin allow-list and no sub-resource filtering with JavaScript enabled, including the one that receives the printer admin password. Seat C deliberately left it **unscored** | C | **ACCEPT — FILE IT** | Filed as **`D-UP-07`**, **Medium**, and **deliberately still unscored** — `n/a`, with the reason and a revisit gate on the row. Band set by this register's own convention for an **absent** control (`I-D9`, `I-D10`, `H-D7`); a vector was **not** invented to fill the column. Mediums +1. |
| 1c | **Split `DELTA-MK-03`** into (a) cleartext-at-rest 4.9 and (b) unmasked-entry 4.3 | D | **ACCEPT** | Split into **`DELTA-MK-03a`** (Medium 4.9) and **`DELTA-MK-03b`** (Medium 4.3); both vectors re-derived independently and both reproduce. Parent row retained as `DELTA-MK-03`, uncounted, pointing at its children. Lows −1, Mediums +2. |
| 1d | **Split `ADM-D3`** into its five distinct configuration weaknesses, keeping the Keycloak-retirement qualifier on each | D | **ACCEPT** | Split into **`ADM-D3a`** (auto-link; base **7.1** recorded, band held at Medium by the reviewer's *Suspected* + retirement qualifiers) and **`ADM-D3b`–`ADM-D3e`** (implicit flow, ROPC, wildcard web origins, 180-day sessions) — **all four deliberately unscored**, because four vectors invented at the split would be the same error seat D refused to make at the bundle. Retirement qualifier carried on every one. **The sixth sub-item, the wildcard `redirectUris`, is measured INERT and recorded on the retained parent rather than filed.** Mediums +3, Lows +1. |
| 1e | **De-count `DELTA-HP-01` and `DELTA-HP-02`** — the delta file's own author wrote *"not as a new finding"* and the register counted them anyway | D | **ACCEPT — MARKED WITHDRAWALS** | Both rows retained and marked **WITHDRAWN**, de-counted (Low −1, Informational −1). **A counting error was withdrawn, not an observation:** `send.js` is still anonymous, unbounded and schema-less, the raw error disclosure is still real, and both are still printed and should still be fixed. |
| 1f | **`ADM-D5` Low to Medium 5.3** — a Medium-band number under a `Low` band with no reason recorded anywhere. Depends on **INFRA-02**, which fell in no seat's partition | D | **ACCEPT** | Moved to **Medium 5.3**. **The INFRA-02 dependency is NOT closed by this ruling** — if it does not hold, `AC:H` gives 3.7 and the row returns to Low, **and the reason must then be written down rather than the band merely restored.** Lows −1, Mediums +1. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 6.3 Open items

**Action.** Re-measure the inert-gitleaks claim across all thirty-two repositories before any of it is published to a customer, and give the re-measurement an owner. No partition could see it, so no partition can close it.

**Open item 1 — the estate-wide inert-gitleaks claim is understated, and no single reviewer could
see it.** Set out in full at §3.3.1. The estate-wide conclusion should be re-measured across all
repositories before it is published to a customer. **This is the clearest cost of the parallelism, it
was worth paying, and it needs an owner.**

**Action.** Settle `PR` for an Android `normal` permission once, estate-wide, against HPAM's own declaration of `TokenLibraryPermission`, and apply the answer to this row and to the unfiled MailFlow instance of the same defect together. The partition owner's Low stands until then.

**Open item 2 — `D-SP-04`: one metric decides the band and no reviewer could settle it.** The
partition owner re-derived at source and kept `PR:L`, giving 3.6 and a Low, refuting round 1's
predicted move up to Medium. Another reviewer's out-of-partition note argues `PR:N`, on the ground
that an Android `normal` permission is auto-granted at install and is therefore not a privilege, and
**on `PR:N` this row computes 4.0, a Medium.** That reviewer explicitly disclaimed the note as not
their verdict. **The partition owner's verdict is applied; the tension is recorded rather than
resolved.** The same question sets the ceiling on the unfiled MailFlow instance of the same defect,
and both depend on HPAM's own declaration of `TokenLibraryPermission`, which is a third component.

**Action.** Leave the applied **High 7.1** in place, and fire the revisit gate written onto the row only on the live tenant verified-domain check — by evidence, not by argument.

**Open item 3 — `NEW-5` (License-Services) was applied over an out-of-partition lead pointing the
other way.** One reviewer's handover read the filed Medium as a reasoned hold pending a live tenant
verified-domain check, which is held. The partition owner re-derived every metric at source, found the
vector entirely sound, and moved the row to **High 7.1**, answering that concern directly on the
ground that `AC:H` already prices exactly that uncertainty. The first reviewer disclaimed their own
note, so the partition owner's verdict is applied, and **the revisit gate is written onto the row** so
that it can be undone by evidence rather than by argument. It is recorded because it is the one
applied band move where another reviewer's material pointed the other way.

**Action.** Put the question to the client rather than to a reviewer: is a deliberate environmental bucketing to Critical still the position Datasec wants to publish, given that the base is 7.7 and the finding is conditioned on MFA being off? **This is a judgement about a signed-off customer deliverable, not a scoring correction, and the band stays Critical until the client rules.**

**Open item 4 — June `F-02`: a proposed downgrade was refused, and it is worth a Critical.** A
verification reviewer moved `F-02` from Critical to High at 7.7 and called it the highest-stakes call
in the report. **Its arithmetic is right and is independently reproduced: the row's own vector gives
7.7, and Critical is reachable only if `AC:L` and `PR:N` hold together, since every single-concession
reading computes 8.7, a High.** The band move does not follow from that, because of the ground given
for it — that no scoring note records a deliberate business bucketing, unlike four other rows that
say so in writing. **There is one, and it says so in writing, in the same words.** At the end of
`F-02`'s Verification block the June register reads: *"Environmental note: severity is bucketed
Critical above its 7.5 base because this is a privacy/identity-authenticator confidentiality failure
in a defence/regulated context … if MFA is enforced tenant-wide the write path is not taken and
severity drops toward High/Medium, whereas any deployment running MFA-off keeps it Critical."* That
is the identical construction credited to another row. It lives in the Verification block rather than
in a Scoring note, which is exactly why a search of the scoring notes missed it.

**The discriminating test, stated so that the next reviewer can apply it rather than re-argue it:** a
note that **names the base and says the band is deliberately above it** is a bucketing decision and
must not be "fixed"; a note that **argues the band from the number** is a band that followed a number,
and correcting the number moves the band. `F-02` is the first kind; `F-07` and `F-10` are the second,
which is why those two were applied and this one was not. The base number was corrected from 7.5 to
7.7, the full metric-space table was recorded, the bucketing note was promoted so that a reader meets
it, and **the band stays Critical.**

**What is genuinely open, and it is a question for the client rather than a scoring question:** is a
deliberate environmental bucketing to Critical still the position Datasec wants to publish, given
that the base is 7.7 and the whole finding is conditioned on MFA being off? That is a judgement about
a signed-off customer deliverable, and it is not one a verification reviewer should take by silently
downgrading a Critical.

**Action.** Assign an owner one reading of `CreateClientRequest.cs:40` and a decision on whether to file it. The finalising reviewer is not authorised to raise findings on their own initiative, which is why it is recorded here and on the retained `ADM-D3` row rather than counted.

**Open item 5 — a seventh Keycloak provisioning weakness, named and not filed.**
`CreateClientRequest.cs:40` hardcodes `FullScopeAllowed = true` as a get-only default on **every**
client the administration portal provisions, which places the full set of realm roles in every token
those clients issue. It is not one of the five weaknesses ruled on, no reviewer's partition scoped it,
and the finalising reviewer is not authorised to raise findings on their own initiative. It is
recorded here and on the retained `ADM-D3` row rather than counted. **It needs an owner and one
reading.**

**Action, and it is the most urgent item any reviewer raised.** Treat every credential cited in `F-16` and `F-12` as disclosed and rotate on that basis, independently of the repository remediation; re-issue that register with values replaced by the structural references this document uses throughout; and establish where the current `.docx` and `.md` have already been distributed. The three steps are set out below; **the third is the client's.**

**Open item 6 — handling of the June register itself. This is not a scoring matter and it is the
most urgent item any reviewer raised.** `Deliverables/03_Findings_Register.md`, a signed-off,
customer-facing deliverable that is also rendered to `.docx`, **prints secret values verbatim.**
Reported structurally: eight distinct lines inside the Evidence blocks of `F-16` and `F-12`, covering
Entra client secrets, a platform API key, an App Configuration connection-string secret, a PFX
private-key password and service and administrative password literals. **No value, prefix, length or
redacted head is reproduced here.** The finding that documents committed secrets **reproduces them
into a document with wider and less controlled distribution than the source repository**, which means
**F-16's remediation is incomplete by construction:** rotating the committed secrets does not address
the report, and purging repository history does not either.

Recommended, and this is document handling rather than a register edit: **(i)** treat every credential
cited in `F-16` and `F-12` as disclosed and rotate on that basis, independently of the repository
remediation; **(ii)** re-issue that register with values replaced by the structural references — file,
line, credential class — that this document uses throughout, and the findings lose nothing; **(iii)**
establish where the current `.docx` and `.md` have already been distributed. **No verifier has checked
whether any of these credentials is still live**; that needs a live pass, which is held. **This is a
reported disclosure, not a confirmed active compromise, and the handling recommendation stands
regardless of validity, because the document cannot be un-distributed.** Item (iii) is the client's.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 6.4 What was verified personally at source

Not the whole population. The following were read at their cited `file:line`, reading the code rather
than the reviewer's summary: F-01, F-02, F-06, F-11, F-12, F-13 (the escalation), F-16, F-19, F-21,
F-23, F-24, F-26; the HP-AuthSuite hardcoded device credential; both HP-AuthSuite TLS bypasses; the
HPSA identity (`com.hp.secureauth`); the HPSA hardcoded QR key; the HPSA password-assurance search
with its control; the `infra-administration-portal` twenty-seven-value inventory, `UseEncryption` and
`[AllowAnonymous]`; and the `.gitleaks.toml` correction.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 6.5 What is not done

1. **Nothing has been re-scored against a live environment.** Every environmental CVSS adjustment on
 the reachability-dependent findings still needs the deferred live GitHub, Azure and Entra pass.
2. **Two live checks are named by reviewers as the next action**, both in the companion register's
 scope but affecting shared conclusions: whether the OneTimePad demonstration exposes `/setup`
 unauthenticated, and whether Entra genuinely pins the EAM subject.
3. **No dependency-CVE delta is offered.** June ran `trivy` 0.71 over nineteen components; this run
 ran 0.74 over thirty-two. Two variables moved at once, the database and the population, and the
 population grew roughly fivefold. Neither number is a trend.
4. **Twenty-three rows still carry no CVSS vector** — the twenty-two rows of §3.4 and the one row of
 §3.5. Their 2026-09-08 pass verified severity bands and their stated bases, not the arithmetic of
 the scores, and no round-2 partition covered them.
5. **Several rows carry explicit revisit gates that a single live datum would fire:** `I-D1`,
LicenseServer `NEW-5`, `H-D3`, `D-SP-02`, `D-07`, `DELTA-MK-01`, `DELTA-MK-04` and `DELTA-HP-01`.
6. **Blocked on access, and none of these needs a tenant:** the HPAM client's verification code, which
 closes `NEW-1`'s gap; the **License Portal source**, which closes `DELTA-MK-01` and `DELTA-MK-04`
 at once; the **WorkPath bundle**, which closes `WP-D1` and whose `restore_from_bundles.sh` must be
 fixed first per `WP-D2`; **INFRA-02** in `infra-administration-portal-main`, which settles `ADM-D1`
 and `ADM-D5` together; and the off-origin navigation trace that scores `D-UP-07`.
7. **`WP-D1`'s secret content still rests on June's extraction** and no bundle was opened.

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 7. Appendices

```{=openxml}
<w:p/><w:p/><w:p/>
```

### Appendix A — Testing methodology

The assessment was a static, read-only source-code and configuration review. No source was modified,
nothing was executed, and no live, production or customer system was contacted. Secrets are reported
structurally — file, line, variable and credential class — and never by value.

The methodology draws on published frameworks:

- OWASP Application Security Verification Standard (ASVS)
- OWASP API Security Top 10
- OWASP Mobile Application Security Verification Standard (MASVS) and the Mobile Top 10
- Common Vulnerability Scoring System v3.1 (CVSS 3.1)
- NIST Cybersecurity Framework 2.0, and SP 800-53 and SP 800-63
- ISO/IEC 27001:2022
- GDPR and the Australian Privacy Principles
- The MITRE Common Weakness Enumeration (CWE)

Three automated instruments were run across all thirty-two components — `gitleaks` for secret
scanning, `semgrep` for static analysis and `trivy` for dependency and configuration scanning — and
every automated result was confirmed or refuted by reading the source. Where code and documentation
disagreed, the code was treated as authoritative.

**Verification discipline.** Every finding raised by a reviewer was re-derived at source by a second
reviewer who did not write it and who was instructed to falsify it. Negative claims — statements that
a control is absent — require a positive control demonstrating that the same instrument, at the same
scope, does find the thing when it is present. Where a verifier produced a CVSS score, they first
wrote a CVSS 3.1 implementation from the specification and validated it against published reference
vectors before any number was trusted.

**How commands, searches and evidence are presented.** Every command, search pattern, path, file
reference and code literal in this document is set in a monospace face and is visually distinct from
the commentary around it: **inline** where it sits inside a sentence, and **in its own block** where
it stands alone. Where a finding rests on a **negative** claim — that a control is absent — the search
and its **positive control** are shown together in a block, so that a reader can see both the question
that was asked and the proof that the instrument would have answered it differently had the thing been
present. This follows the discipline of the reference reports and of published security-reporting
practice: an absence is only evidence when the instrument that failed to find it is shown to work.

**What the methodology does not cover.** No dynamic testing, no penetration testing, no live
configuration reading, and no decompilation of vendored binary artefacts.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### Appendix B — Vulnerability ratings

Severity is expressed as a CVSS 3.1 base score and its band, except where a row states that its band
is a deliberate business or environmental bucketing above or below its base. Where that is the case,
the row says so and gives the base. **Such rows must not be "corrected"to match their number.**

| Band | CVSS 3.1 base | Meaning |
|---|---|---|
| **Critical** | 9.0 – 10.0 | Requires immediate attention and a plan for action. The event may cause severe reputational damage, severe financial loss, or a severe impact on operations, information availability, assets or individuals. |
| **High** | 7.0 – 8.9 | Urgent, and in most circumstances will pose a serious threat or consequence. The event may cause significant reputational damage, significant financial loss, or a major impact on operations, information availability, assets or individuals. |
| **Medium** | 4.0 – 6.9 | Less urgent, but in some circumstances may still pose a serious threat or consequence. The event may cause moderate reputational damage, moderate financial loss, or a moderate impact on operations, information availability, assets or individuals. |
| **Low** | 0.1 – 3.9 | Not an imminent threat, but should be addressed to avoid issues in the longer term. The event may cause minor financial loss or a minor impact on operations, information availability, assets or individuals. |
| **Informational** | n/a | No demonstrated security impact in this snapshot. Recorded because it is latent, because it bears on assurance, or because it is a documentation or configuration observation that a future change could make live. |

**Findings deliberately carrying no numeric score.** Where a control does not fire, or a posture
baseline is not met, a base score misrepresents the finding. Those rows carry no number and state the
reason instead: `n/a, posture finding`, `n/a, control failure`, `n/a, assurance finding`, `n/a,
architectural aggregate, not additive`, or `n/a, unscoreable from this repository`.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### Appendix C — Reconciliation of the estate total

The table below reconciles the **estate** total across both registers. It is retained unchanged
because it is the audit record of how the total moved, and because every step in it was measured
rather than asserted. **The per-register figure is in §1.2; this table is the combined figure.**

| Step | C | H | M | L | I | Total |
|---|---|---|---|---|---|---|
| **Before this session** (register as built 2026-09-08 07:28) | 21 | 65 | 81 | 52 | 23 | **242** |
| Verification pass moves D-CVL-02 and D-CVL-03 Medium to Low (§2.3) — *no change to the total* | 21 | 65 | **79** | **54** | 23 | **242** |
| **+ §2.3.3 — batch-1 delta findings, 62** | +3 | +11 | +30 | +11 | +7 | **+62** |
| Subtotal — the commissioned scope | **24** | **76** | **109** | **65** | **30** | **304** |
| **Verification pass 2026-09-09 moves `H-D1` Critical to High (§2.3.3)** — *no change to the total* | **23** | **77** | 109 | 65 | 30 | **304** |
| **+ §2.3.4 — the eight "Done" components' delta findings, 34** | +0 | +4 | +11 | +12 | +7 | **+34** |
| **+ §2.3.5 — SPDF-D1, raised by the ITEM 4 coverage-gap review** | +0 | +1 | +0 | +0 | +0 | **+1** |
| Subtotal — the position published on 2026-09-09 before round 2 | **23** | **82** | **120** | **77** | **37** | **339** |
| **ROUND 2 CONSOLIDATION 2026-09-09 — seat A** · `D-01`, `I-D1`, `I-D2` High-to-Critical · `I-D8` Low-to-Medium · `D-07` Low-to-Informational | **+3** | **−3** | **+1** | **−2** | **+1** | **±0** |
| **ROUND 2 — seat B** · `NEW-2` LS High-to-Medium · `NEW-5` LS Medium-to-High · `NEW-6` LS Low-to-Medium · `NEW-9` SRV Low-to-Medium | 0 | 0 | **+2** | **−2** | 0 | **±0** |
| **ROUND 2 — seat C** · `H-D2` High-to-Low · `D-SP-02` Medium-to-Low · `D-UP-01`, `D-UP-02` Medium-to-Informational *(the `D-MF-01` withdrawal was held here and is RULED below)* | 0 | **−1** | **−3** | **+2** | **+2** | **±0** |
| **ROUND 2 — seat D** · `DELTA-MK-02` Medium-to-High *(the `MK-03`/`ADM-D3` splits, `ADM-D5` and the `hpam-api` de-count were held here and are RULED below)* | 0 | **+1** | **−1** | 0 | 0 | **±0** |
| **ROUND 2 — seat J (June baseline)** · `F-07` High-to-Critical · `F-10` High-to-Critical *(`F-02` Critical-to-High was proposed and is **NOT APPLIED** — see the FINALISE line below and §2.3.7 open item 9)* | **+2** | **−2** | 0 | 0 | 0 | **±0** |
| Subtotal — the position published 2026-09-09 after round 2, with `F-02` corrected | **28** | **77** | **119** | **75** | **40** | **339** |
| **FINALISE 2026-09-09 — ruling 1a** · `D-MF-01` **WITHDRAWN** *(row retained and marked; de-counted)* | 0 | **−1** | 0 | 0 | 0 | **−1** |
| **FINALISE — ruling 1b** · `D-UP-07` **FILED** — UniversalPrint auth WebViews, no origin gate | 0 | 0 | **+1** | 0 | 0 | **+1** |
| **FINALISE — ruling 1c** · `DELTA-MK-03` **SPLIT** into `03a` 4.9 and `03b` 4.3, both Medium | 0 | 0 | **+2** | **−1** | 0 | **+1** |
| **FINALISE — ruling 1d** · `ADM-D3` **SPLIT** into `ADM-D3a` … `ADM-D3e` | 0 | 0 | **+3** | **+1** | 0 | **+4** |
| **FINALISE — ruling 1e** · `DELTA-HP-01` and `DELTA-HP-02` **WITHDRAWN** *(rows retained and marked; de-counted)* | 0 | 0 | 0 | **−1** | **−1** | **−2** |
| **FINALISE — ruling 1f** · `ADM-D5` Low to **Medium 5.3** | 0 | 0 | **+1** | **−1** | 0 | **±0** |
| **ESTATE TOTAL** | **28** | **76** | **126** | **73** | **39** | **342** |

**Both sums were computed independently.** By row, across the seven contributing populations:
188 + 31 + 22 + 1 + 62 + 37 + 1 = **342**. By column, across the five severity bands:
28 + 76 + 126 + 73 + 39 = **342**. **It balances both ways, and no cell was adjusted to make it
balance.** The three section tallies were re-added independently against their own tables: batch 1 is
62, the pre-limit set is 37, and the coverage-gap review is 1.

**Five rows are printed and not counted, and none was deleted:** three marked withdrawals
(`D-MF-01`, `DELTA-HP-01`, `DELTA-HP-02`) and two retained split parents (`DELTA-MK-03`, `ADM-D3`).

**This register's share of the estate**, re-added independently from the same populations:
18 Critical + 49 High + 80 Medium + 40 Low + 23 Informational = **210**. The companion Datasec
register carries 10 + 27 + 46 + 33 + 16 = **132**. **210 + 132 = 342**, and the two registers agree
with the estate total band by band.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### Appendix D — Engagement record

This appendix holds the record of how the coverage of this engagement was established. It is retained
because the coverage question is itself an assurance question, and because the decisions in it were
argued and reversed rather than simply taken.

**Coverage of the June-baseline delta set is closed at nineteen of nineteen.** Eight components were
delta-reviewed on 2026-09-07 before the session limit, seven more in batch 1, and four in batch 2,
which was commissioned after the client reversed a recommendation to drop them. Each of the nineteen
has its own delta file. HPSM was never one of the nineteen: it has no June baseline.

**The recommendation that was reversed, recorded because the reasoning matters more than the
outcome.** The coordinating reviewer recommended dropping the remaining eleven components on the
ground that re-reading components June had already covered was the lowest-value use of a budget that
had already been exhausted once that day. **The client overruled it.** The argument against that
recommendation was the stronger one: the gap sat precisely in the class of defect that scanners
cannot see, which is where every Critical of the run came from, and two of the eleven were already
implicated by findings stumbled upon rather than sought. The gap analysis was right; the
recommendation drawn from it was not. That reversal produced batch 1 and batch 2, and therefore
closed the coverage gap.

**What the gap cost while it was open, bounded honestly.** It was never a claim that the eleven
unreviewed components were clean; nobody had looked for new defects in them. It was partially
mitigated, and by a measurable amount: all three scanners ran across all thirty-two components
including those eleven, and all thirty-one June findings were re-verified at source, so pattern-class
and known-finding coverage was current. What was missing was the class scanners cannot see —
authorisation logic, trust decisions, fail-open paths, cross-component seams and configuration — and
that is exactly where the run's Criticals came from.

**Consolidation was three times the size anyone had stated.** Batch 1's findings existed only as
narrative; they are now filed as sixty-two counted rows. Measuring that gap then revealed that the
eight components listed as "done" had unfiled findings too, and those are now filed as a further
thirty-seven rows. **Ninety-six findings, including three Critical rows as filed, had been carried in
working files and counted nowhere**, so every total published before that point understated the
estate. The commissioning brief had estimated the gap at *"roughly twenty"*; it was measured, not
estimated, at ninety-six.

**The identifier list this engagement carried was also wrong**, and it is recorded because it is the
same class of error as several findings in this register. It named three identifier series and a
fourth that does not exist, and it named none of the other series in play. The full census is in §3.6
and §3.7.

---

*End of register. Client Confidential.*
