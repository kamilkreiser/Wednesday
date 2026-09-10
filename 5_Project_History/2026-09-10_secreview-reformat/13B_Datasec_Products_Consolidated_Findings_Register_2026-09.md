# Consolidated Findings Register — Datasec Product Portfolio

**Independent Security Assessment of the Datasec Product Portfolio**
Prepared by Datasec Solutions Pty Ltd on behalf of Datasec
Version 3.1 · Release date 9 September 2026 · **Client Confidential**

```{=openxml}
<w:tbl><w:tblPr><w:tblStyle w:val="Table"/><w:tblW w:type="dxa" w:w="9412"/><w:tblLayout w:type="fixed"/><w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="0" w:val="0020"/></w:tblPr><w:tblGrid><w:gridCol w:w="3000"/><w:gridCol w:w="6412"/></w:tblGrid><w:tr><w:trPr><w:tblHeader w:val="on"/></w:trPr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="3000"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Document control</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="6412"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve"></w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="3000"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Created</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="6412"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">07/09/2026</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="3000"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Effective date (current version)</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="6412"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/09/2026</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="3000"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Next review date</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="6412"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">March 2027, or on completion of the deferred live-configuration pass</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
<w:p><w:pPr><w:pStyle w:val="BodyText"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Revision history.</w:t></w:r><w:r><w:t xml:space="preserve"> This document is version-controlled. All changes are recorded below.</w:t></w:r></w:p>
<w:tbl><w:tblPr><w:tblStyle w:val="Table"/><w:tblW w:type="dxa" w:w="9412"/><w:tblLayout w:type="fixed"/><w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="0" w:val="0020"/></w:tblPr><w:tblGrid><w:gridCol w:w="820"/><w:gridCol w:w="1180"/><w:gridCol w:w="2100"/><w:gridCol w:w="5312"/></w:tblGrid><w:tr><w:trPr><w:tblHeader w:val="on"/></w:trPr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Version</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Edit date</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Author</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">Summary of amendments</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">2.0</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">07/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">First review of the Datasec product portfolio, as part of the 2026-09 re-run.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">2.1</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">08/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent verification pass, one verifier per component. Coverage-gap review adds one finding.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">2.2</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Round-2 consolidation. Every band and score re-derived at source.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">3.0</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Reissued as two registers on the client’s instruction. Presentation only.</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="820"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">3.1</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="1180"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">09/09/2026</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2100"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Independent Security Review</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5312"/></w:tcPr><w:p><w:pPr><w:pStyle w:val="Compact"/></w:pPr><w:r><w:t xml:space="preserve">Title page, clickable contents, section page breaks, body aligned to the reference report, every finding restructured on BLUF. No finding, severity, score, vector or count changed.</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
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
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X220e8142f6cd4a8d04f6b8e2b499874ddf0dfeb"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">1.4 How the counts are constructed</w:t></w:r></w:hyperlink></w:p>
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
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X7b5156d3b36deff07c08cc29371560866ef0238"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.2 Critical findings</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X72a3d8518ccf5b26a9587b26cf70bd56743d35d"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.3 Per-component tally</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xdf72931f799d1d558b88245d1d12904795d2b28"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.4 Delta review, Task-Dispatcher</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X048d4cdd70da904dfa8889ecf5a26b119144101"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.5 Coverage-gap review</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xa3592aeceda358a082ae7e405c983d473198da0"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">3.6 Commercial and product-claim observations</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X2565cdd1c70bc07e88c127ab4409e38943f9818"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">4. Verification Status and Open Items</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X5e5e672c1c4f5ece2fb69b3d233d0dbcd4b5b1d"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">4.1 The per-component verification pass</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xe9d78b9ad6668693c03372e27deef5e50306d5d"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">4.2 Open items</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X7806e35dab77ce238c6ce2bf8632cb2236f25e3"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">4.3 What is not done</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X111a18b47734bed804c3f2a639488d646f744eb"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">4.4 What was verified personally at source</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X7721be68407a11a24c4285b331d248da842f2ad"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">5. Assurance Observations</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="Xa9b740c802b7ff6dfa59e51b77ebebeb07c4e40"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">6. Keycloak Position</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC1"/><w:ind w:left="0"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X8cf020d2cfbf480e417545296e44ec21fed2773"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">7. Appendices</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="appendix-a--testing-methodology"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">Appendix A — Testing methodology</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="appendix-b--vulnerability-ratings"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">Appendix B — Vulnerability ratings</w:t></w:r></w:hyperlink></w:p>
<w:p><w:pPr><w:pStyle w:val="TOC2"/><w:ind w:left="360"/><w:spacing w:after="0"/></w:pPr><w:hyperlink w:anchor="X4cae5ef2c0beee2d92dae3146981fbdbcced036"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">Appendix C — Reconciliation of the estate total</w:t></w:r></w:hyperlink></w:p>
<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>
```

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 1. Executive Summary

Datasec commissioned an independent security review of its own product portfolio alongside the HP
Authentication Suite engagement. This register covers **nine Datasec-owned products**: the CypherKey
passwordless identity provider, myPKI, SecurePDF, the Cryptix secure document-exchange portal, the
NexusAI reporting dashboard, the Task-Dispatcher internal automation tool, the HPSM repository
scaffold, and the two parked commercial tools, Vision Sales Portal and QuickQuote. Eight of the nine
had **never previously been assessed**; they were ruled into scope by the client on 7 September 2026.

The review was conducted as a **static, read-only source-code and configuration assessment** against
industry frameworks — OWASP ASVS, the API Security Top 10, MASVS and the Mobile Top 10, NIST CSF 2.0
and SP 800-53/63, ISO 27001:2022, and GDPR and the Australian Privacy Principles — with each finding
scored under CVSS 3.1. No live, dynamic or penetration testing was performed, and no production or
customer system was contacted. This matters particularly for Vision Sales Portal, which has a live
production instance: it was **not** touched, and every conclusion about it is drawn from source
alone. Every finding is cited to source as `file:line`, and where code and documentation disagreed,
the code was treated as authoritative.

**This register records 132 findings across the Datasec product portfolio: 10 Critical, 27 High, 46
Medium, 33 Low and 16 Informational.** The dominant themes are unauthenticated administrative and
data-access surfaces, committed secret material, authentication subjects taken from client-controlled
input, and authentication that fails open. Two products carry defects at the centre of their own
stated purpose: an identity provider that accepts a caller-supplied subject on one of its three
federation surfaces, and a secure document-exchange portal whose entire action API is
unauthenticated.

**These are first-time findings.** Nothing in this register has had a remediation cycle, and none of
it should be read as a regression.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.1 Overall risk ratings, by Target of Evaluation

Based on the discovered vulnerabilities, the following risk ratings are allocated to each product.

| Target of Evaluation | Risk rating | Most severe findings |
|---|---|---|
| CryptixWebPortal (secure document exchange, TokenOne) | **Critical** | CRYPTIX-01, -02, -03, -04 |
| OneTimePad, product name **CypherKey** (passwordless IdP) | **Critical** | OTP-01, OTP-27 |
| NexusAI / Reporting Dashboard AU | **Critical** | RD-01 |
| myPKI (face-biometric key generation and personal PKI) | **Critical** | MYPKI-01 |
| SecurePDF (certificate-encrypted PDF pipeline) | **Critical** | SPDF-01, `SPDF-D1` |
| Vision Sales Portal *(parked)* | **Critical** | VSP-01 |
| Task-Dispatcher (internal developer automation) | **Medium** | F-31, F-27, `TD-D1` |
| QuickQuote *(parked)* | **High** | see §3.3 |
| HPSM (HP Security Playbook web platform) | **Not assessable** | repository scaffold only; there is no code to review |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.2 Severity distribution

```
Critical       ##########                                      10
High           ###########################                     27
Medium         ##############################################  46
Low            #################################               33
Informational  ################                                16
               ----------------------------------------------    
TOTAL                                                         132
```

The register is built from four distinct populations of work. They are listed separately because they
were produced by different methods and carry different levels of verification; the distinction
matters when reading any single row.

| Population | Critical | High | Medium | Low | Informational | **Total** |
|---|---|---|---|---|---|---|
| June 2026 baseline register, re-derived at source 2026-09-09 | — | — | 2 | — | — | **2** |
| Components reviewed for the first time in the 2026-09 re-run | **10** | **26** | 43 | 31 | 13 | **123** |
| Delta review, the components reviewed before the 2026-09-07 session limit | — | — | 1 | 2 | 3 | **6** |
| Coverage-gap review, re-derived at source 2026-09-09 | — | **1** | — | — | — | **1** |
| **TOTAL — this register** | **10** | **27** | **46** | **33** | **16** | **132** |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.3 Key findings

The dominant themes are summarised below. Full detail, evidence and remediation for each finding
follow in §3.

- **An identity provider takes the authenticated subject from a client-controlled form field.** The
CypherKey EAM connector issues the signed identity token using the subject supplied in the request
 body, after testing only that the challenge succeeded. The other two federation surfaces in the
 same product do this correctly, which is what makes it a defect rather than a design. The only
 stated safeguard is a code comment. An attacker holding a victim's password — the first factor this
 product exists to survive — satisfies a challenge with their own device and submits the victim's
 subject (OTP-01, CVSS 9.6).
- **A secure document-exchange portal's entire action API is unauthenticated.** All sixty-eight
`actions/` endpoints are open, including the unwrap endpoint, which takes a caller-supplied
 envelope identifier, fetches that envelope's decryption password on the caller's behalf, decrypts
 the wrapper and returns the files with web URLs — the exact inverse of the product's purpose.
Alongside it: twenty-three unauthenticated administrative actions including company deletion; three
 unauthenticated upload paths into the web root with the filename sanitiser commented out; and a
 database of per-tenant API and signing keys served from the web root (CRYPTIX-01 to -04).
- **Authentication fails open on a marketplace product.** NexusAI's `requireAuth` returns early when
 enforcement is not yet enabled, leaving all 175 routes unauthenticated. This occurs on every fresh
 deployment until setup completes **and** from the outer error handler on any storage error, so a
 correctly configured instance reverts to fully open on a storage hiccup. Ingress is external
 (RD-01).
- **Committed secret and key material across the portfolio.** A Cosmos DB primary master key is
 committed at HEAD inside a shipped desktop application (SPDF-01), and ten accounts' passwords are
 upserted from plaintext in source on every boot of the Vision Sales Portal, with no environment
 guard and no password-change mechanism anywhere in the tree (VSP-01).
- **A PKI product's key derivation is weaker than its documentation implies, and the position is more
 nuanced than first filed.** The legacy enrolment path derives keys with no work factor and is still
 shipped; the current path does use a key-derivation function with independent entropy. The finding
 and its correction are set out together at §3.2, and a rescore is **proposed, not applied**, because
 a single verifier should not move a published Critical downward unreviewed.
- **SecurePDF's encryption is addressed to unvalidated recipients.** The encoder validates no
 recipient certificate and reads recipient public keys straight out of the same Cosmos database
 whose master key is committed. Write access to that store substitutes a recipient's certificate and
 silently reads every document encrypted for them afterwards. **Rotation alone does not fix it**
 (`SPDF-D1`, and it enlarges SPDF-01).

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.4 How the counts are constructed

**The estate total across both registers is 28 Critical, 76 High, 126 Medium, 73 Low and 39
Informational, totalling 342.** This register holds 132 of those findings and the companion HP
Authentication Suite register holds 210. **Every finding appears in exactly one register.**

**One estate finding is cross-cutting and is counted in the companion register, not here.** June
`F-21` — the absence of SDLC security gates — records its own affected component as *"All
repositories, CI/CD across the suite"*. Its conclusions apply to the repositories in this register
too, and its consequence for this portfolio is that the committed secrets recorded above could reach
the repositories and stay there. **It is counted once, in the HP Authentication Suite register, and
is referenced here without being counted again**, so that the two registers sum correctly.

**Provenance of the per-component figures.** They are as reported by each reviewer and then
independently re-derived per component; the verification table is at §4.1. A sample was verified
personally at source, listed in §4.4. Treat any single row as Confirmed only where its own entry says
so.

**One published figure was corrected rather than silently edited.** The NexusAI row originally read
eighteen findings with five Low; it is seventeen with four Low. A reviewer's seed file carried a
summary line that overcounted Low by one, and it was relayed without the items being counted; the
project's own agent counted them — seventeen headings, a tally summing to seventeen, with controls on
both sides — and corrected it. **Findings in that component are cited `SEC-01` to `SEC-17`, never as
bare `RD-nn`, because `RD` is also the Jira project key and the numbers collide.**

**A second correction, also recorded rather than absorbed.** The parked-pair row of the estate summary
formerly printed five cells that summed to ten rather than to their own stated total of seventeen.
The corrected cells are Vision `1/1/3/2/1` = 8 and QuickQuote `0/1/3/4/1` = 9, giving `1/2/6/6/2` = 17
for the pair. This was forced independently two ways, and **no total changed; the estate total was
never affected.** The published severity split for the parked pair had been wrong by one High, three
Medium, two Low and one Informational.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 1.5 Important caveats

- **This is a point-in-time assessment.** It is a static review of a provided source snapshot. Because
 exploitation was reasoned rather than performed, in order to avoid any production impact, an
 attacker with greater time and resources may surface issues not identified here. The snapshot may
 also lag the live deployment.
- **Two products are parked.** Vision Sales Portal and QuickQuote were parked by the client on
2026-09-07. Their findings are recorded in full and counted, and they are marked as parked
 throughout. Vision is pre-production per the client, but **the credentials committed to its
 repository still require rotation, because they are in the repository.**
- **HPSM has no code.** It is carried as "scaffold only, nothing to assess", deliberately **not** as a
 component with zero findings, which would read as a clean bill of health.
- **Two findings need one live check each and cannot be closed without it:** whether the CypherKey
 demonstration deployment actually exposes `/setup` unauthenticated, and whether Entra genuinely
 pins the EAM subject. Both are named by reviewers as the next action.
- **A naming collision affects how findings must be read.** The product actually called **CypherKey**
 lives in a folder named `OneTimePad`, while a folder named `CypherKey` holds a different product
 entirely — HPSA, HP Secure Authentication, which belongs to the companion register. A finding
 labelled "CypherKey" is ambiguous between two authentication products, and the plain-language
 reading is the wrong one. Findings in this register use the product identity, not the folder name.

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 2. Overview

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.1 Background

The June 2026 assessment covered nineteen components, all of them part of the HP Authentication
Suite. On 7 September 2026 the client ruled thirteen further components into scope, instructing that
the review *"include the new projects and run the full test, not just high level"*. Eight of those
thirteen are Datasec's own products and are covered here; a ninth product, Task-Dispatcher, had been
in the June scope as supporting internal tooling and its findings are carried here with it.

**The re-run's central result bears on this register directly.** The June review covered nineteen of
thirty-two components and therefore measured about a fifth of the estate. The thirteen components it
never saw hold eighty per cent of the third-party dependency surface — 1,780 of 2,198 packages — and
produced fifteen Critical findings, none of which existed in any register beforehand. **Ten of those
fifteen are in this register.**

All testing was performed against a provided source snapshot. No live system was contacted.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.2 Register of findings

| Section | Population | Findings | Verification status |
|---|---|---|---|
| §3.2 | Critical findings | 10 Critical rows, drawn from the 123 findings in the first-time reviews | Independently re-derived per component |
| §3.3 | Per-component tally | 123 | Independently re-derived per component |
| §3.4 | Delta review, Task-Dispatcher | 6 | Re-derived at source in round 2 |
| §3.5 | Coverage-gap review, SecurePDF | 1 | Re-derived at source 2026-09-09 |
| §3.6 | Commercial and product-claim observations | Not severity-scored | Measured, with controls |
| §1.2 | June 2026 baseline register, Task-Dispatcher rows | 2 | Re-derived at source 2026-09-09 |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.3 In scope

Testing covered the following Targets of Evaluation, all as provided source.

- **`OneTimePad`** — product name **CypherKey**: a ground-up .NET rebuild of the patented TokenOne
KeyMap strong two-factor and passwordless authentication system, with an authentication server, an
Entra EAM / OIDC / SAML connector, an administration portal, native iOS and Android clients and
Bicep infrastructure as code.
- **`CryptixWebPortal`** — the legacy Datasec secure document-exchange portal, TokenOne
 authenticated.
- **`myPKI`** — face-biometric deterministic key generation and a personal PKI and provenance stack.
- **`SecurePDF`** — a Windows print-to-encrypted-PDF pipeline using myPKI certificates.
- **`Reporting_Dashboard_Au`** — **NexusAI**, an Azure Marketplace print-analytics dashboard with an
LLM assistant.
- **`Task-Dispatcher`** — internal developer-productivity automation, explicitly unrelated to the HP
Authentication Suite runtime.
- **`HPSM`** — the HP Security Playbook web platform. **Repository scaffold only: two files, no
 application code.**
- **`vision_datasec-sales-portal`** — Vision Sales Portal *(parked 2026-09-07)*.
- **`vision_hpas-quickquote`** — QuickQuote *(parked 2026-09-07)*.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.4 Testing methodology

Please refer to Appendix A for testing-methodology details, and to Appendix B for the severity rating
scheme.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 2.5 Out of scope

- Remediation of any vulnerability discovered.
- Denial-of-service and performance testing.
- Live, dynamic or penetration testing of any deployed environment. **No production, staging or
 customer system was contacted, including the live Vision Sales Portal instance.**
- The live GitHub, Azure and Entra configuration pass, which is deferred.
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
for the Datasec product projects. A finding is assigned to **this** register when its affected
component is a **Datasec-owned product** rather than a component of the HP Authentication Suite,
judged from that component's own technical summary and manifest rather than from whether the prose
mentions a product name. Nine of the thirty-two components under review meet that test, and they are
listed in §2.3. The remaining twenty-three are carried in
`13A_HPAM_Consolidated_Findings_Register_2026-09`. **Every finding appears in exactly one of the two
registers, and the two sum to the estate total of 342.**

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

| Section in the superseded register | In this register (Datasec) | In the companion register (HPAM) |
|---|---|---|
| §1 Per-component tally | §3.3 | §3.2 |
| §2 The fifteen new Critical findings | §3.2 | §3.2 |
| §2.1 Verification pass | §4.1 | §6.1 |
| §2.2 Findings that change earlier conclusions | — | §3.3 |
| §2.3 Delta review, batch 2 | — | §3.4 |
| §2.3.2 Bearer-scheme sweep | — | §3.5 |
| §2.3.3 Delta review, batch 1 | — | §3.6 |
| §2.3.4 Delta review, the pre-limit components | §3.4 | §3.7 |
| §2.3.5 Coverage-gap review | §3.5 | — |
| §2.3.6 Reconciliation of the estate total | Appendix C | Appendix C |
| §2.3.7 Round-2 consolidation and open items | §4.2 | §6.2 and §6.3 |
| §3 What was verified personally at source | §4.4 | §6.4 |
| §4 Commercial and product-claim observations | §3.6 | §3.8 |
| §5 Assurance observations | §5 | §4 |
| §6 Keycloak retirement position | §6 | §5 |
| §7 What is not done | §4.3 | §6.5 |
| §7.1 Delta-review coverage record | — | Appendix D |


```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.2 Critical findings

**The numbering below is the estate-wide Critical index and is preserved so that cross-references
elsewhere in the assurance pack remain valid; it is not a per-document sequence.**

**Summary of the Critical findings in this register.** The full record for each — the issue, the suggested fix, and below them what was tested, how it was tested and how to resolve it — follows the table, one finding to a block.

| # | Component | Severity | Finding |
|---|---|---|---|
| 1 | OneTimePad *(product: CypherKey)* | **Critical** · CVSS 9.6 | The EAM connector takes the authenticated subject from a client-controlled form field |
| 2 | OneTimePad *(product: CypherKey)* | **Critical** | `/setup` bypasses the portal's only gate, and there are no `[Authorize]` attributes anywhere in the portal |
| 3–6 | CryptixWebPortal | **Critical** | The 68-endpoint `actions/` API is entirely unauthenticated, including the endpoint that decrypts secure wrappers |
| 11 | Reporting Dashboard (NexusAI) | **Critical** | `requireAuth` fails open, leaving all 175 routes unauthenticated |
| 13 | myPKI | **Critical** *(rescore proposed, not applied)* | Private keys derive from a public biometric plus an unstretched passphrase — **and the correction to that claim must be read with it** |
| 14 | SecurePDF | **Critical** | An Azure Cosmos DB primary master key is committed at HEAD inside a shipped desktop application |
| 15 | Vision Sales Portal *(parked)* | **Critical** | Ten accounts' passwords are upserted from plaintext in source on every boot |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 1 — The EAM connector takes the authenticated subject from a client-controlled form field

| Finding **Critical 1** | **Critical** · CVSS 3.1 **9.6** · component **OneTimePad** *(product name **CypherKey**)* |
|---|---|
| **The issue** | **EAM connector takes the authenticated subject from a client-controlled form field.** `EamController.cs:158` issues the signed `id_token` with `form.Subject` (`[FromForm(Name="sub")]`, `:294`) after testing only `result.Succeeded`. The other two federation surfaces do it correctly (`FederatedIdpController.cs:104,110`; `SamlController.cs:303-308`) — which is what makes it a defect, not a design. **The only stated safeguard is a code comment at `:155` ("Entra pins it").** An attacker holding a victim's Entra password — the first factor this product exists to survive — satisfies a challenge with their own phone and submits the victim's `sub`. |
| **Suggested fix** | Derive the subject from the challenge result — `result.Subject` — exactly as the OIDC and SAML paths in the same product already do, and reject on any mismatch with a submitted hint rather than trusting the form. |
| **What was tested** | The **OneTimePad** authentication server and its three federation surfaces — EAM, OIDC and SAML — as provided in the source snapshot. The claim under test: that the EAM path takes the subject from the request body while the other two take it from the challenge result. Artefacts read at the cited lines: `EamController.cs:155,158,294` · `FederatedIdpController.cs:104,110` · `SamlController.cs:303-308` · `EamIdTokenIssuer.ResolveAcr`. |
| **How it was tested** | Static, read-only source review of the provided snapshot, followed by an independent verification pass by a reviewer who did not raise the finding: thirty-two confirmations, no refutations, three down-scores and two up-scores for this component (§4.1). **Verified at source by Wednesday**, including the two correct counterparts, which is what establishes that this is a defect rather than a design decision. **One thing was not tested and cannot be, statically:** whether Entra genuinely pins the EAM subject, which is the only claimed safeguard. That is one of the two live checks named as the next action (§4.2, open item 2). Until it is answered, **the safeguard remains a code comment.** |
| **How to resolve** | (1) Derive the subject from the challenge result — `result.Subject` / `result.SubjectId` — exactly as the OIDC and SAML paths already do. If a hint echo is required by the EAM protocol, compare `result.Subject` to the hint's `sub` and **reject on mismatch** rather than trusting the form. (2) Re-validate the `id_token_hint` on the verify POST, or carry a server-side record of the validated hint keyed by `challenge_id` from the authorize step, and take `sub` and `acr` from that record. (3) Resolve `acr` through `EamIdTokenIssuer.ResolveAcr` on the verify path so that the honest-`acr` allow-list actually applies. (4) Answer the live question of whether Entra pins the subject, and record the answer on this row — it decides whether the defect is exploitable today or only latent. *(Recorded by the reviewer who raised the finding, in `findings-seed-2026-09/onetimepad-main.md`, `OTP-01`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 2 — `/setup` bypasses the portal's only gate, and no `[Authorize]` attribute exists anywhere in the portal

| Finding **Critical 2** | **Critical** · component **OneTimePad** *(product name **CypherKey**)* |
|---|---|
| **The issue** | `/setup` uses `@layout EmptyLayout`, bypassing the portal's only gate; **zero `[Authorize]` attributes anywhere in the portal**; with no session the API client attaches the portal's own `X-Admin-Key`, and the server registers that scheme whenever the deployment is not hardened — which the demonstration deployment is not. |
| **Suggested fix** | Put a real authorisation gate on the portal rather than relying on a layout — the portal has none at all — and stop registering the admin-key scheme in any deployment that is reachable from outside. |
| **What was tested** | The **OneTimePad** administration portal and the authentication server's scheme registration, as provided in the source snapshot. The claim under test: that the layout is the portal's only gate, that no `[Authorize]` attribute exists anywhere in it, and that the admin-key scheme is registered when the deployment is not hardened. Artefacts read: the `/setup` page and its `@layout EmptyLayout` declaration · the portal's API client and its `X-Admin-Key` attachment · the server's scheme registration and its hardening guard. |
| **How it was tested** | Static, read-only source review of the provided snapshot, followed by an independent verification pass by a reviewer who did not raise the finding (§4.1). The `[Authorize]` absence is a census over the portal's source, not a sample. **This row is the one Critical in this register that is not closed statically:** whether the demonstration deployment actually exposes `/setup` unauthenticated **needs one live check against the running demo**, and that check is held. It is named as the next action at §4.2, open item 2. **The code defect is established; the exposure is not.** |
| **How to resolve** | (1) Add a real authorisation gate — `[Authorize]` with a policy, applied at the pipeline rather than per page — so that a layout choice cannot bypass it. (2) Do not register the `X-Admin-Key` scheme in any deployment reachable from outside; if a bootstrap path is required, bind it to a one-time token that expires when setup completes. (3) Serve only the setup wizard until first-run completes, and 401 everything else, rather than leaving the gate open globally. (4) Run the live check on the demonstration deployment and record the result on this row, because it decides whether this is an exposure today or a latent defect. *(Derived from the finding as measured; the source review file records the defect, and the exposure question is recorded as an open item rather than answered.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 3–6 — The 68-endpoint `actions/` API is entirely unauthenticated

| Finding **Critical 3–6** | **Critical** · component **CryptixWebPortal** |
|---|---|
| **The issue** | The **68-endpoint `actions/` API is entirely unauthenticated**, including `unwrap.php`, which takes a caller-supplied envelope UUID, fetches that envelope's decryption password on the caller's behalf, decrypts the wrapper and returns the files with web URLs — the exact inverse of the product's purpose. Plus: 23 unauthenticated `admin2` actions (including `delete-company`); three unauthenticated upload paths into the web root with the filename sanitiser commented out; and a SQLite database of per-tenant TokenOne API and signing keys served from the web root. |
| **Suggested fix** | If the App Service is live, take it offline or put it behind an authenticating proxy **before any code change**, then add the authentication bootstrap the component already contains at two files to every endpoint under `actions/`, and rotate every credential in the exposed key database. |
| **What was tested** | The **CryptixWebPortal** PHP application, as provided in the source snapshot: the `actions/` endpoint set, the `admin2` dispatcher, the three upload paths, and the committed key database. The claim under test: that no authentication guard runs on those endpoints. Artefacts read at the cited lines: every file under `actions/` (68) · `admin2/endpoints.php:7` and its 23 handlers · `upl.php`, `upload.php:56` and `views/content/reply/` · `admin2/tokenone_keys.db` · the two files that *do* carry the guard, `download.php:10` and `remove_file.php:9-10`, which are the positive control. |
| **How it was tested** | Static, read-only source review of the provided snapshot — the endpoint set was enumerated, not sampled — followed by an independent verification pass by a reviewer who did not raise the finding: twenty-eight confirmations, no refutations, one down-score and **three new findings raised by the verifier** (§4.1). **Verification made one of these worse rather than better:** the exposed key database holds **nineteen rows, not roughly eight** (§4.1.2). The two guarded files are what make the absence a measurement rather than an impression: the pattern exists in this codebase and is simply not applied to the other sixty-eight. |
| **How to resolve** | (1) **Immediately, and before any code change:** if the App Service is live, take it offline or put it behind an authenticating reverse proxy or App Service Easy Auth. This is not a code-fix-first finding. (2) Add a single `require_once` bootstrap to every file under `actions/` that calls `checkPortalLoggedIn()` — and `restrictReaderPermission()` where privilege matters — **before any other statement**; the pattern already exists at `download.php:10` and `remove_file.php:9-10`. (3) Add an ownership check in `unwrap.php`, `file-unwrap.php` and `advancedUnwrap.php`: verify the session user is a recipient or creator of that UUID before decrypting. (4) Insert an `Auth::isLoggedIn()` guard in `admin2/endpoints.php` immediately after `include_once "bootstrap.php"`, returning 401 for everything except the three login actions, and add a role check on the company-scoped actions; add CSRF tokens at the same time, because the dispatcher accepts `$_REQUEST` and every action is therefore also reachable by GET. (5) Delete `upl.php` and `views/content/reply/` outright — both are legacy and the current UI uses `upload.php`; on `upload.php`, add the login check as the first statement, re-enable the commented sanitiser at `:56`, add a positive extension allow-list, move the target directory outside the document root, and validate the UUID. (6) Treat all nineteen rows of the key database as compromised and rotate them at the provider; delete the database, the `forbidden/` and `restricted/` directories and both log files from the repository, then purge them from history. *(Recorded by the reviewer who raised the findings, in `findings-seed-2026-09/cryptixwebportal-main.md`, `CRYPTIX-01` to `CRYPTIX-04`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 11 — `requireAuth` fails open, leaving all 175 routes unauthenticated

| Finding **Critical 11** | **Critical** · component **Reporting Dashboard AU (NexusAI)** |
|---|---|
| **The issue** | **`requireAuth` fails open** — `backend/server.js:2287-2292`, `if (!authEnforced) return next()`, all 175 routes unauthenticated. This occurs on every fresh deployment until setup completes **and** from the outer `catch` on any `jsonStorage` error, so a correctly configured instance reverts to fully open on an Azure Files hiccup. Ingress is `external: true`. |
| **Suggested fix** | Invert the default so that `isAuthEnforced()` returns `true` unless it can positively read a stored `false`, make the `catch` return `true`, and bound the open window structurally by serving only the first-run wizard until setup completes. |
| **What was tested** | The **Reporting Dashboard AU** (NexusAI) backend and its Azure Marketplace deployment template, as provided in the source snapshot. The claim under test: that the guard returns early when enforcement is not enabled, that the same state is reachable from an error path, and that ingress is external. Artefacts read at the cited lines: `backend/server.js:2287-2292` and the 175 route registrations · `isAuthEnforced()` and its storage read · the outer error handler · `mainTemplate.json` and its `external: true` ingress. |
| **How it was tested** | Static, read-only source review of the provided snapshot, followed by an independent verification pass by a reviewer who did not raise the finding: fifteen confirmations, no refutations, one down-score and one up-score for this component (§4.1). **Verified at source by Wednesday.** **Verification made this finding worse in a way that matters to whoever fixes it:** the fail-open behaviour is confirmed, but **the finder's stated mechanism for the second path was wrong — it is not the outer error handler — so a fix written against the report as filed would have missed it** (§4.1.2). The count of routes and the ingress setting were read rather than accepted. |
| **How to resolve** | (1) **Invert the default.** `isAuthEnforced()` must return `true` unless it can positively read a stored `authEnforced === false`, and the `catch` must return `true`, not `false`. (2) **Bound the open window structurally.** Before first-run completes, serve *only* the first-run wizard and its `/api/setup/` routes and 401 or redirect everything else — do not `next()` past the gate globally. (3) **Add a platform layer** so the application is not the only thing standing between the internet and the data: add a `Microsoft.App/containerApps/authConfigs` resource to `mainTemplate.json` with Entra and `unauthenticatedClientAction: Return401`, or bind `ipSecurityRestrictions` to the customer's ranges. (4) Fix the second path against the mechanism the verifier established, not the one the finding as filed described. *(Recorded by the reviewer who raised the finding, in `findings-seed-2026-09/reporting-dashboard-au-main.md`, `RD-01`, with the mechanism corrected at verification.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 13 — Private keys derive from a public biometric plus an unstretched passphrase — with the correction that must be read alongside it

| Finding **Critical 13** | **Critical** · component **myPKI** · **rescore to High proposed 2026-09-08 and deliberately NOT applied** |
|---|---|
| **The issue** | *As filed:* "Every private key the product issues derives from `SHA-512(face_descriptor + '\|' + password)` — no KDF, no work factor, no stretching (`keyGenerator.js:15-33`). The face descriptor is public information *by the product's own premise*, so the key reduces to an unstretched passphrase, brute-forceable offline. For a PKI product this is the defining defect." **What re-derivation at source found is that the word "every" is false for the current path**, and the three defects the finding should become are set out under *how to resolve* below. |
| **Suggested fix** | Replace the legacy derivation with a memory-hard key-derivation function and a real per-enrolment random salt, and separately fix the current path's password-derived salt — **but do not close this row on the rescore until a second reader has reviewed it**, because a single verifier should not move a published Critical downward unreviewed. |
| **What was tested** | The **myPKI** key-generation and enrolment paths, as provided in the source snapshot: the legacy `deriveSeed` branch and the current v2, v3 and v4 regeneration paths. The claim under test: that *every* issued private key derives from an unstretched hash of a public descriptor and a password. Artefacts read at the cited lines: `keyGenerator.js:15-33` · `server.js:404-410` (v4 multibit fuzzy-commitment enrolment), `:545-595` (`generateKeysFromSeed`), `:648-667` (the legacy branch, response tagged `_legacy`) · `stableSeed.js:816-818,860,874-882` · `bchCommitment.js:37-40,42-49,52-60`. |
| **How it was tested** | Static, read-only source review of the provided snapshot, followed by an independent verification pass by a reviewer who did not raise the finding: twelve confirmations, no refutations, one down-score (§4.1). **This is the single largest correction of the whole verification pass** (§4.1.1). The verifier read the fuzzy-commitment mathematics the finder had not read, and established that on all three current paths `seed = SHA256(K) XOR PBKDF2(password, salt, 10000, 32, 'sha256')` where **K is `crypto.randomBytes`, not the face** — so there *is* a key-derivation function with a work factor and independent entropy, and the key does not reduce to `SHA-512(descriptor\|password)`. The cited `deriveSeed` survives only in the legacy branch. **What decides High versus Critical was not testable here:** how many deployed records still use the legacy path is a live question the tenant hold blocks. **The rescore is proposed, not applied, and the row stands at Critical** (§4.2, open item 1). |
| **How to resolve** | **Three defects, which is what this finding should become.** (1) The legacy enrolment path is still shipped and still behaves exactly as filed — replace the `SHA-512` chain with a memory-hard KDF (Argon2id, or scrypt with N ≥ 2^17) and a per-enrolment random salt stored beside the commitment, and migrate or retire the legacy records. **How many deployed records are legacy is the live question that decides this row's band.** (2) `derivePasswordHash` uses **`SHA256(password)` as the salt** (`stableSeed.js:816-818`, duplicated at `bchCommitment.js:37-40`) — a password-derived salt is not a salt — and 10,000 PBKDF2-SHA256 iterations is far below current guidance; give it an independent random salt and raise the work factor. (3) An attacker holding a stored record **and** the public descriptor recovers `K` by the scheme's own decode, after which the seed reduces to brute-forcing that weak PBKDF2 — so the work factor in (2) is load-bearing, not cosmetic. **Publish an explicit entropy budget for the seed phrase and enforce it at enrolment, and state in the product documentation that the biometric contributes *stability*, not *secrecy*.** **A second reader is needed before the rescore is applied; everything they need is cited here.** *(Recorded by the reviewer who raised the finding, in `findings-seed-2026-09/mypki-main.md`, `MYPKI-01`, and corrected in `_Working/2026-09-08_ITEM4_COVERAGE_GAPS.md`, GAP 2.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 14 — An Azure Cosmos DB primary master key is committed at HEAD inside a shipped desktop application

| Finding **Critical 14** | **Critical** · component **SecurePDF** |
|---|---|
| **The issue** | **Azure Cosmos DB primary (master) key** committed at HEAD (`myPKI_Printer/app.config:5`; **length deliberately not reproduced**) with its endpoint, shipped inside a desktop application. **The blast radius is larger than "rotate".** That same container is the **unvalidated trust root for document encryption**: `spdf_encode` validates no recipient certificate, and the caller feeds it `PublicKey` values read straight out of this database (see `SPDF-D1`, §3.5). Write access substitutes a recipient's certificate and silently reads every document afterwards encrypted for them. **Rotation alone does not fix it** — without certificate validation, any future write access to that store reproduces the attack. |
| **Suggested fix** | Rotate the Cosmos key and replace it with Entra authentication and data-plane RBAC — a desktop application should never hold an account master key — and, because rotation alone does not fix it, validate recipient certificates in the encoder as well (`SPDF-D1`). |
| **What was tested** | The **SecurePDF** printer client, console and encoder, as provided in the source snapshot. The claim under test: that the committed value is an account master key rather than a scoped token, and that the same container is the source of the recipient public keys the encoder trusts. Artefacts read at the cited lines: `myPKI_Printer/app.config:5` (credential class and location reported structurally; **no value, prefix or length reproduced**) · `myPKI_Printer/RecipientSource.cs:15,18,45-66` · `myPKI_Console/Program.cs:57-65,67-96` · `myPKI_Printer/DemoForm.cs:76,152-157,169-190`. |
| **How it was tested** | Static, read-only source review of the provided snapshot, followed by an independent verification pass by a reviewer who did not raise the finding: nine confirmations, no refutations (§4.1). The link to the encoder's missing validation was established by the coverage-gap review on 2026-09-08 and re-derived at source on 2026-09-09, with a control that fires: certificate-validation vocabulary over every `*.cs` in the component returns **zero** matches, against a positive control of thirteen certificate-handling hits in three projects (§3.5). **What was not tested:** whether the account is live, whether the key is current, and what the container actually holds — there was no Azure access under the holds. |
| **How to resolve** | (1) **Treat as compromised.** Rotate the Cosmos key — rotate the secondary, cut over, then rotate the primary — and purge it from git history, or accept and document that it remains there. (2) Replace it with **Entra ID authentication and data-plane RBAC roles**, or at minimum a scoped resource token issued by a server the client authenticates to. **A desktop application should never hold an account master key.** (3) Add a gitleaks rule for `.config` files: the repository's `.github/workflows/gitleaks.yml` exists and did not stop this. (4) **Rotation alone does not fix the exposure**, because the same store is the unvalidated trust root for encryption — apply `SPDF-D1`'s remediation, which is to validate recipient certificates in the encoder, and note that **that fix survives the other two.** *(Recorded by the reviewer who raised the finding, in `findings-seed-2026-09/securepdf-master.md`, `SPDF-01`, and enlarged by `SPDF-D1` at §3.5.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### Critical 15 — Ten accounts' passwords are upserted from plaintext in source on every boot

| Finding **Critical 15** | **Critical** · component **Vision Sales Portal** *(parked 2026-09-07)* |
|---|---|
| **The issue** | *`server/seed.js` upserts ten accounts' passwords — eight `datasec_admin`, six named individuals — from plaintext in source on **every boot**. Imported as `seedIfEmpty` but the SQL is `ON CONFLICT … DO UPDATE SET password_hash`; no `NODE_ENV` guard, while the `SESSION_SECRET` guard 140 lines earlier is production-aware. No password-change mechanism exists in the tree.* **Pre-production per the client; the credentials still require rotation because they are in the repository.** |
| **Suggested fix** | Change all ten passwords out of band now, then add the production guard that the `SESSION_SECRET` check 140 lines earlier already demonstrates, and remove the plaintext passwords from source. |
| **What was tested** | The **Vision Sales Portal** server, as provided in the source snapshot. **No live system was contacted**, including the live production instance — every conclusion here is drawn from source alone. The claim under test: that the seed runs on every boot rather than only when the table is empty, and that no environment guard prevents it. Artefacts read at the cited lines: `server/seed.js` and its `ON CONFLICT … DO UPDATE SET password_hash` clause (passwords reported structurally, never reproduced) · `scripts/create-azure-user.js` · `index.js:27-35`, the production-aware `SESSION_SECRET` guard used as the internal control. |
| **How it was tested** | Static, read-only source review of the provided snapshot. **Verified at source by Wednesday.** The internal control is what makes the missing guard a measurement rather than an impression: the same file family contains a production-aware guard 140 lines earlier, so the pattern was understood by the authors and simply not applied here. The name `seedIfEmpty` was not taken at face value — the SQL was read, and it upserts. **This component is parked, and its findings are recorded and counted in full and marked as parked throughout** (§1.5). |
| **How to resolve** | In priority order. (1) **Change all ten passwords on the production instance now, out of band, and treat every one as compromised.** (2) Add a `NODE_ENV` or `WEBSITE_SITE_NAME` guard so `seedIfEmpty()` cannot run in production, mirroring the guard already at `index.js:27-35`. (3) Remove the plaintext passwords from `server/seed.js` and `scripts/create-azure-user.js`; generate a random password per account at seed time and print it once, or require it from the environment. (4) Build a password-change endpoint and force a change at next login — **there is currently no password-change mechanism anywhere in the tree.** (5) Purge from git history, or accept and document. (6) Consider placing the portal behind an authenticating front door. **Being parked does not defer (1) or (5):** the credentials are in the repository whatever the deployment status. *(Recorded by the reviewer who raised the finding, in `findings-seed-2026-09/vision-datasec-sales-portal-main.md`, `VSP-01`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.3 Per-component tally

| Component | Product identity | C | H | M | L | I | Total |
|---|---|---|---|---|---|---|---|
| CryptixWebPortal | Datasec doc-exchange portal (TokenOne) | **4** | 8 | 10 | 6 | 2 | 30 |
| OneTimePad | **brand: CypherKey** — passwordless IdP | **2** | 7 | 14 | 10 | 3 | 36 |
| Reporting Dashboard AU (**= NexusAI**) | reporting + Azure Marketplace | **1** | 4 | 6 | 4 | 2 | 17 |
| myPKI | PKI product | **1** | 4 | 4 | 3 | 1 | 13 |
| SecurePDF | PDF encryption (NOT signing — see §4) | **1** | 1 | 3 | 2 | 2 | 9 |
| HPSM | scaffold only — **nothing to assess** | — | — | — | — | 1 | 1 |
| *Vision Sales Portal* | *PARKED 2026-09-07* | *1* | *1* | *3* | *2* | *1* | *17* |
| *QuickQuote* | *PARKED 2026-09-07* | *—* | *1* | *3* | *4* | *1* | *(both)* |

The parked pair is tallied jointly in the total column: Vision Sales Portal contributes eight
findings and QuickQuote nine, giving seventeen for the pair.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.4 Delta review, Task-Dispatcher

Task-Dispatcher was one of the eight components delta-reviewed on 2026-09-07 before the session
limit. Those reviews produced findings that had been carried in working files and counted nowhere;
they were filed as counted rows on 2026-09-08 and **all have since been independently re-derived at
source** in round 2. **Severities below are not transcribed; they are re-derived, and the vector is
recorded beside the score wherever a verifier produced one.**

**Summary of the findings in this section.** The full record for each — the issue, the suggested fix, and below them what was tested, how it was tested and how to resolve it — follows the table, one finding to a block.

| ID | Component | Severity | CVSS 3.1 | Finding |
|---|---|---|---|---|
| TD-D1 | Task-Dispatcher | Medium *(bucketed "env-adjusted")* | **8.7 base** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` | The consumer side of the pipeline is also unauthenticated: the Cursor rule executes whatever answers on `localhost:4901`, so any local process that binds… |
| TD-D2 | Task-Dispatcher | Low | **3.5** `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N` | Unauthenticated HTTP callers can inject arbitrary Markdown into the operator's Telegram "approval channel" |
| TD-D3 | Task-Dispatcher | Low *(reason now recorded)* | **4.2** `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:L` *(a Medium-band number, and the Low is deliberate)* | `callback_query` handler lacks the chat-id gate that the message handler applies |
| TD-D4 | Task-Dispatcher | Info | — | Informational: `git add -A` by an autonomous agent on a developer working tree |
| TD-D5 | Task-Dispatcher | Info | — | Informational: precision on F-27's form-data claim |
| TD-D6 | Task-Dispatcher | Info | — | Informational: configuration observations |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### TD-D1 — The consumer side of the pipeline is also unauthenticated: the Cursor rule executes whatever answers on `localhost:4901`, so any local process that binds the port feeds tasks into the autonomous deploy path

| Finding `TD-D1` | **Medium *(bucketed "env-adjusted")*** · CVSS 3.1 **8.7 base** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` · component **Task-Dispatcher** |
|---|---|
| **The issue** | The consumer side of the pipeline is also unauthenticated: the Cursor rule executes whatever answers on `localhost:4901`, so any local process that binds the port feeds tasks into the autonomous deploy path |
| **Suggested fix** | Give the dispatcher a per-install shared secret that the rule must present, have the rule verify the responder before trusting it, and remove the session-start auto-run. |
| **What was tested** | The **Task-Dispatcher** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/task-dispatcher-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Test record.** *[2026-09-09: **confirmed outright — vector, arithmetic and bucket all correct.** The base 8.7 reproduces exactly and the Medium is a documented environmental adjustment from a High base, now recorded on the row instead of being invisible behind a `—`.]* |
| **How to resolve** | (1) Give the dispatcher a per-install shared secret and have the rule send it (`Authorization: Bearer $TASK_DISPATCHER_TOKEN` from the developer's env) — the server must reject without it (this also closes F-31's server side). (2) Have the rule verify the responder: e.g. `GET /api/health` must return a signed nonce or a known instance id stored outside the repo. (3) Remove `alwaysApply`/session-start auto-run; make task pickup an explicit, human-invoked action. (4) Keep the F-31 remediations (loopback bind is *not* sufficient against a local squatter — a token is). *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/task-dispatcher-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### TD-D2 — Unauthenticated HTTP callers can inject arbitrary Markdown into the operator's Telegram "approval channel"

| Finding `TD-D2` | **Low** · CVSS 3.1 **3.5** `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N` · component **Task-Dispatcher** |
|---|---|
| **The issue** | Unauthenticated HTTP callers can inject arbitrary Markdown into the operator's Telegram "approval channel" |
| **Suggested fix** | Authenticate the POST routes, escape or drop Markdown in relayed bodies, and include the task's original instruction hash so the operator can see what was executed. |
| **What was tested** | The **Task-Dispatcher** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/task-dispatcher-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Test record.** *[2026-09-09: **confirmed outright — vector and arithmetic exact.**]* |
| **How to resolve** | Auth on the POST routes (TD-D1/F-31); escape or drop Markdown in relayed bodies (`parse_mode` off for the result line, or MarkdownV2 with escaping); include the task's *original* instruction hash so the operator can see what was actually executed. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/task-dispatcher-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### TD-D3 — `callback_query` handler lacks the chat-id gate that the message handler applies

| Finding `TD-D3` | **Low *(reason now recorded)*** · CVSS 3.1 **4.2** `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:L` *(a Medium-band number, and the Low is deliberate)* · component **Task-Dispatcher** |
|---|---|
| **The issue** | `callback_query` handler lacks the chat-id gate that the message handler applies |
| **Suggested fix** | Apply the same `chatId` gate at the top of the `callback_query` handler, and check the sender against an operator allow-list. |
| **What was tested** | The **Task-Dispatcher** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/task-dispatcher-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Test record.** **[2026-09-09: confirmed, arithmetic corrected 3.7 to **4.2 — which CROSSES A BAND — and the Low is nonetheless RETAINED, with its reason now written on the row.** The asymmetry is cleanly measured: `telegramBot.js:81` (message handler) has `if (String(cid) !== String(chatId)) return;` and `:153-154` (callback handler) goes **straight into the `sp:`/`ok:`/`cl:`/`cx:`/`ct:` branches with no comparison at all** — the check is present next door, so its absence here is a measurement. **Two reasons the band stands: (1) the vector double-counts one precondition** — `AC:H` and `UI:R` both encode the single fact that the attacker can only see a bot message with an inline keyboard if it leaves the operator's chat, and removing either raises the score further (`UI:N` to 4.8), which shows 3.7 was understated twice over rather than that 4.8 is right; **(2) the real impact does not reach Medium in substance** — the reachable branch is `ct:`, cancelling a queued task the operator can simply re-queue. **The reviewer's judgement is better than either number, and a defence-in-depth gap correctly filed as Low should not be promoted by arithmetic alone.** *(Contrast `ADM-D5`, where the same shape got the opposite recommendation because the substance differs: there an attacker corrupts an audit trail the operator relies on, and no qualifier exists anywhere.)* **NOT TESTED: whether Telegram delivers a `callback_query` from a forwarded message at all — the exploitability gate, and it is a live check that is held.**]** |
| **How to resolve** | Apply the same `chatId` gate at the top of the `callback_query` handler; additionally check `cbq.from.id` against an operator allow-list. *(Recorded by the reviewer who raised the finding, in `delta-review-2026-09/task-dispatcher-main.md`.)* |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### TD-D4 — Informational: `git add -A` by an autonomous agent on a developer working tree

| Finding `TD-D4` | **Info** · no CVSS score recorded · component **Task-Dispatcher** |
|---|---|
| **The issue** | `git add -A` by an autonomous agent on a developer working tree. |
| **Suggested fix** | Run `gitleaks` as a local pre-commit hook inside the rule — the repository already runs it in CI, so this closes the gap for free — and replace `git add -A` with an explicit path list. |
| **What was tested** | The **Task-Dispatcher** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/task-dispatcher-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Test record.** *[2026-09-09: confirmed exactly (`check-tasks-workflow.mdc:111`, run after every task and pushed to `main` without review; `:81` `az webapp up` in the same sequence). **Correctly Informational and no vector should be assigned** — there is no attacker and no impacted component in the CVSS sense; the harm is a developer's untracked credential file being swept into a push. **It is nonetheless the sharpest remediation in this component: the repo already runs gitleaks in CI, and running it as a local pre-commit hook inside the rule would close this for free.**]* |
| **How to resolve** | Replace `git add -A` with an explicit path list, and run `gitleaks` as a local pre-commit hook inside the rule. The repository already runs `gitleaks` in CI, so the rule set exists and this costs nothing. **Correctly Informational and deliberately unscored** — there is no attacker and no impacted component in the CVSS sense; the harm is a developer's untracked credential file being swept into an automated push. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### TD-D5 — Informational: precision on F-27's form-data claim

| Finding `TD-D5` | **Info** · no CVSS score recorded · component **Task-Dispatcher** |
|---|---|
| **The issue** | precision on F-27's form-data claim. |
| **Suggested fix** | Correct the register's wording to "not reachable by any code path", which is measured, rather than "not installed", which is not safe to assert while the vulnerable version is a peer dependency npm 7 and later installs by default. |
| **What was tested** | The **Task-Dispatcher** component, as provided in the source snapshot. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/task-dispatcher-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** **Test record.** *[2026-09-09: confirmed — the lockfile was re-read rather than the summary accepted, and the reviewer is right on every point (`request` 2.88.2 **peer**, its nested `form-data` **2.3.3 peer**, top-level `form-data` 4.0.5, `@cypress/request` 3.0.10). Control fires: `require('request')` across all `*.js` returns **zero matches**, positive control `require(` returns 10 hits. **The vulnerable `form-data` 2.3.3 is a peer of `request`, which npm ≥ 7 installs by default, so "not installed" is not safe to assert while "not reachable by any code path" is measured and true — the register's wording should change accordingly.** `F-27` is a June row: measurement recorded, boundary respected, no re-score attempted.]* |
| **How to resolve** | Change the register's wording from "not installed" to "not reachable by any code path". The distinction is not pedantic: the vulnerable `form-data` 2.3.3 is a peer dependency of `request`, which npm 7 and later installs by default, so "not installed" is not safe to assert, while "not reachable" is measured — `require('request')` returns zero matches across all `*.js` against a positive control of ten. `F-27` is a June row and no re-score was attempted. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### TD-D6 — Informational: configuration observations

| Finding `TD-D6` | **Info** · no CVSS score recorded · component **Task-Dispatcher** |
|---|---|
| **The issue** | configuration observations. *[2026-09-09: confirmed — all three sub-items exact.]* |
| **Suggested fix** | Apply the three configuration corrections recorded in the delta file. |
| **What was tested** | The **Task-Dispatcher** component, as provided in the source snapshot. The claim under test: *Informational: configuration observations*. The `file:line` references cited in the issue and in the test record below were read at source; the full working record is `delta-review-2026-09/task-dispatcher-main.md`. |
| **How it was tested** | Static, read-only source review of the provided snapshot. Every row in this section was re-derived at source on 2026-09-08 by an independent verifier who did not write it, by opening the cited file and line, confirming the defect is present as described, and testing the stated basis of its severity. **No CVSS vector string is recorded for any row in this section, so what was verified is the severity band and its stated basis, not the arithmetic of the score.** |
| **How to resolve** | Apply the three configuration corrections recorded in `_Working/delta-review-2026-09/task-dispatcher-main.md`, all three of which were confirmed exactly at verification on 2026-09-09. |

**Tally for this section: 1 Medium, 2 Low and 3 Informational, totalling 6 counted.**

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.5 Coverage-gap review

The coverage-gap work produced one new finding, by closing a gap that an earlier report had named.

**Summary of the findings in this section.** The full record for each — the issue, the suggested fix, and below them what was tested, how it was tested and how to resolve it — follows the table, one finding to a block.

| ID | Component | Severity | CVSS 3.1 | Finding |
|---|---|---|---|---|
| SPDF-D1 | SecurePDF | **High** | **7.1** `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:L` *holds by 0.1* | The encoder trusts any certificate it is handed, and the certificates come from the database whose master key is Critical #14. `spdf_encode` performs no… |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### SPDF-D1 — The encoder trusts any certificate it is handed, and the certificates come from the database whose master key is Critical #14. `spdf_encode` performs no chain validation, expiry check, key-usage check or identity binding on recipient certificates — it encrypts to whatever file it is given

| Finding `SPDF-D1` | **High** · CVSS 3.1 **7.1** `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:L` *holds by 0.1* · component **SecurePDF** |
|---|---|
| **The issue** | **The encoder trusts any certificate it is handed, and the certificates come from the database whose master key is Critical #14.** `spdf_encode` performs **no** chain validation, expiry check, key-usage check or identity binding on recipient certificates — it encrypts to whatever file it is given. The caller reads those certificates from a Cosmos container (`SELECT * FROM c`) reached with the **committed primary (read-write) key** of Critical #14, and passes the record's `PublicKey` straight through. **Write access to that store substitutes a recipient's certificate; every document encrypted for that recipient afterwards is readable by the attacker while the sender's UI still shows the legitimate name.** This **enlarges Critical #14**: that finding is filed as credential exposure, but the same credential is the unvalidated trust root of the product's only security property — **rotation alone does not fix it.** *Caveat, stated because it cuts against the finding:* `RecipientSource.cs:15` reads `AppSettings["EndPointUri"]` while `app.config` declares `EndpointUri`, so that lookup returns null and the DB path may not initialise as shipped in this snapshot; whether the deployed build carries the same typo is not knowable statically. **The encoder's missing validation is unconditional and stands regardless.** |
| **Suggested fix** | Validate recipient certificates in the encoder — chain, validity dates, key usage, and binding to the recipient the sender selected — then rotate the Cosmos key and move it out of the application configuration file. **The first survives the other two.** |
| **What was tested** | The **SecurePDF** component, as provided in the source snapshot. Artefacts read at the cited lines: `myPKI_Console/Program.cs:57-65,67-96` · `myPKI_Printer/DemoForm.cs:76,152-157,169-190` · `myPKI_Printer/RecipientSource.cs:15,18,45-66` · `myPKI_Printer/app.config` (settings named structurally; no value read out) |
| **How it was tested** | Static, read-only source review of the provided snapshot, by construction shape rather than by the word, with a positive control that found both known instances before any zero was believed, plus a constant-consumer sweep for the map-index syntax that the shape search cannot see. **No per-row test record was written for this row**, so the section method above is the whole of what can be said about how it was tested. That is stated rather than filled in. |
| **How to resolve** | **Remediation is one ticket, not three.** Validate recipient certificates in the encoder — chain, validity dates, key usage, and binding to the recipient the sender actually selected — rotate the Cosmos key, and move it out of the application configuration file. **The first survives the other two:** without certificate validation, any future write access to that store reproduces the attack, so rotation alone does not fix it. **Recorded, not filed, and simpler than this finding:** `DemoForm.cs:174` and `SimpleForm.cs:77` set the encoder process file name to a bare name rather than a path, so anyone who can write an executable of that name into an earlier `PATH` entry substitutes the encryption engine outright, with no database access at all. It is deliberately not filed because the install layout and the operator account's `PATH` were not traced. |

**Status: independently re-derived at source on 2026-09-09, confirmed High, and it now carries a
vector.** The control fires, so the absence of validation is a measurement rather than an impression:

```
search   X509Chain|ChainPolicy|Build(|Verify(|CheckValidity|NotAfter|
         NotBefore|KeyUsage|RevocationMode|IsValid|Validate
         over every *.cs in the component (deliberately over-broad)   ->   0 matches

control  X509Certificate|X509CertificateParser|ReadCertificate|PublicKey
         over the same files                                          ->  13 hits, 3 projects
```

There is no certificate validation anywhere in SecurePDF.

**Two metrics are lower than the finding's prose implies, and the verifier said so against their own
interest.** `UI:R` — poisoning the record yields nothing on its own; the attacker obtains plaintext
only when a sender operator afterwards selects that recipient and encrypts a document, which is an
action by a person other than the attacker, and `UI:N` would give 8.2 and would be wrong. `S:U`, with
`S:C` considered and rejected deliberately — the encoder runs as the sender, on the sender's document,
and the recipient store is the *source* of the malicious input rather than a second authority that
suffers; using "the poisoned data comes from elsewhere"to justify `S:C` would be a double count.
`A:L` because the recipient record carries one public-key field, so substitution is a *replacement*
and the legitimate recipient can no longer open the document, bounded because the sender's own
certificate is always added.

**The band is true but fragile, and whoever publishes it should know why.** 7.1 is 0.1 above the
Medium boundary, and `A:L` is the only metric holding it there; with `A:N` it is 6.5, a Medium. This
row is one defensible metric call away from changing band, which no reader of a bare "High" could
possibly tell. **It is the clearest single argument in this engagement for publishing vectors rather
than bands.**

**The finding's own caveat — the one thing it offered as cutting against itself — very probably does
not hold, so the finding is stronger than filed.** The `EndPointUri` / `EndpointUri` case mismatch at
`RecipientSource.cs:15` is real, **but the lookup still resolves**, because .NET application-settings
keys have always been case-insensitive. **Not tested, and marked rather than asserted closed:** there
is no .NET runtime on the review machine and a package restore is a network call under the holds. One
three-line program on any Windows machine converts the finding's only stated weakness into nothing.

**Recorded, not filed — a second defect in the same twenty lines, and it is simpler and stronger than
`SPDF-D1` itself.** `DemoForm.cs:174` and `SimpleForm.cs:77` both set the encoder process file name to
a **bare name rather than a path**, so resolution is left to the `PATH` search, and anyone who can
write an executable of that name into an earlier `PATH` entry **substitutes the encryption engine
outright, with no database access at all.** The deployed install layout and the operator account's
`PATH` were not traced, so it is deliberately **not filed**. Two further executables in the same
product launch a fully caller-supplied file name — the same class, also untraced, also not filed.

**Remediation is one ticket, not three:** validate recipient certificates in the encoder — chain,
validity dates, key usage, and binding to the recipient the sender selected — rotate the Cosmos key,
and move it out of the application configuration file. **The first survives the other two.**

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 3.6 Commercial and product-claim observations

These are recorded because they are product-claim questions before they are security questions. They
are not severity-scored and are not counted in any tally. Each is stated as the issue first and the
suggested action second, with the supporting measurement below it.

**1. SecurePDF does not sign anything.**

| | |
|---|---|
| **The issue** | The product encrypts only, despite its name, and the sender's identity certificate path is declared and never loaded. **This is a product-claim question before it is a security one.** |
| **Suggested action** | Correct the product claim, or implement signing. The claim is contradicted at source rather than merely unevidenced, which is what makes it a claim question. |

The absence is a measurement, not an impression: the search and its positive control were run over
the same files, and the control fires.

```
search   PdfSigner|SignDetached|signature|Verify|CheckValidity
         over all *.cs, *.csproj, *.config   ->   0 hits
control  PdfDocument
         over the same files                 ->  10 hits
```

**2. HPSM has no code.**

| | |
|---|---|
| **The issue** | The repository is a scaffold — two files, no application code. It is carried as "scaffold only, nothing to assess", deliberately **not** as a component with zero findings, which would read as a clean bill of health. |
| **Suggested action** | Keep it recorded as "scaffold only, nothing to assess", and do not let it be reported anywhere as a component with zero findings. |

**3. Two products are called CypherKey.**

| | |
|---|---|
| **The issue** | The folder named `CypherKey` is HPSA, while the folder named `OneTimePad` is CypherKey. A finding labelled "CypherKey" is ambiguous between two authentication products. See §1.5. |
| **Suggested action** | Rename the folders to match the products, and until that is done require every finding, ticket and report to name the product identity rather than the folder name. |

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 4. Verification Status and Open Items

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 4.1 The per-component verification pass

An independent verifier ran per component — **none of them the finder** — each instructed to try to
falsify every finding at source, with five verdicts (confirmed, refuted, downgraded, upgraded,
unverifiable) and a positive control required for every negative claim. All reports are written and
have been read. The table below covers this register's share of that pass.

| Component | CONF | REF | DOWN | UP | UNVERIF | new |
|---|---|---|---|---|---|---|
| OneTimePad | 32 | 0 | 3 | 2 | — | — |
| CryptixWebPortal | 28 | 0 | 1 | — | — | 3 |
| Reporting Dashboard (NexusAI) | 15 | 0 | 1 | 1 | — | — |
| myPKI | 12 | 0 | 1 | — | — | — |
| SecurePDF | 9 | 0 | — | — | — | — |
| **TOTAL** | **96** | — | **6** | **3** | — | **3** |

**Not one finding was refuted.** Across the full pass, 149 findings were re-derived at source by
someone who did not write them and was told to break them, and **none collapsed.** Twelve were
over-scored and were corrected downward; five were under-scored; three cannot be settled without a
live system. **The register is conservative, not inflated.**

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 4.1.1 Movements in the Critical count

| Movement | Finding | Basis |
|---|---|---|
| **OUT** | **MYPKI-01** (Critical 9.3 to **High 8.0**) | The verifier read the fuzzy-commitment maths the finder had NOT read. The live enrolment path is `SHA256(random 78-bit K) XOR PBKDF2-SHA256(pw, 10 000 iterations)` (`bchCommitment.js:37-4x`) — **there IS a KDF and there IS independent entropy.** The finder's "no KDF, no stretching" is wrong for the live path. This is the single largest correction of the pass. |

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 4.1.2 Where verification made findings worse

- **CRYPTIX-04** — the exposed key database holds **nineteen rows, not roughly eight**.
- **RD-01** — the fail-open behaviour is confirmed, but the finder's stated mechanism was wrong: the
 second path is not the outer error handler. **A fix written against the report would have missed.**

```{=openxml}
<w:p/><w:p/><w:p/>
```

#### 4.1.3 Corrections to the coordinating reviewer's own figures

- The stated eighteen findings for NexusAI **is seventeen**, corrected by the project's own count.
This is the same failure as several findings in this register — an instrument whose scope did not
 match the question.

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 4.2 Open items

**Action.** Commission a second reader for the myPKI rescore. Everything they need is cited on the row at §3.2. **The rescore is not applied and the row stands at Critical until they have read it.**

**Open item 1 — the myPKI Critical carries a proposed rescore that has not been applied.** Set out in
full on the row at §3.2. A single verifier should not move a published Critical downward unreviewed;
**a second reader is needed, and everything they need is cited on the row.** What decides High versus
Critical is a live question the holds currently block: **how many deployed records still use the
legacy enrolment path.**

**Action.** Run the two live checks — whether the CypherKey demonstration deployment exposes `/setup` unauthenticated, and whether Entra genuinely pins the EAM subject — and record both results on their rows. Until the second is answered, `OTP-01`'s only stated safeguard is a code comment.

**Open item 2 — two findings need one live check each.** Whether the CypherKey demonstration
deployment actually exposes `/setup` unauthenticated, and whether Entra genuinely pins the EAM
subject. Until the second is answered, OTP-01's only stated safeguard remains a code comment.

**Action.** Treat the credentials cited in the June register as disclosed and rotate on that basis. This is a client action rather than a register edit, and the full item is recorded in the companion HP Authentication Suite register.

**Open item 3 — handling of the June register. This is not a scoring matter and it is the most urgent
item any reviewer raised.** `Deliverables/03_Findings_Register.md`, a signed-off, customer-facing
deliverable that is also rendered to `.docx`, **prints secret values verbatim** — eight distinct
lines inside the Evidence blocks of two findings. **No value, prefix, length or redacted head is
reproduced here.** That register belongs to the HP Authentication Suite engagement and the full item
is recorded in the companion register; it is noted here because the recommended handling — treat the
cited credentials as disclosed and rotate on that basis — is a client action rather than a register
edit, and because it establishes the standard this register holds itself to: **secrets are reported
structurally, never by value.**

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 4.3 What is not done

1. **Nothing has been re-scored against a live environment.** Every environmental CVSS adjustment on
 the reachability-dependent findings still needs the deferred live GitHub, Azure and Entra pass.
2. **The two live checks at open item 2 are the named next action.**
3. **No dependency-CVE delta is offered.** June ran `trivy` 0.71 over nineteen components; this run
 ran 0.74 over thirty-two. Two variables moved at once, the database and the population, and the
 population grew roughly fivefold. Neither number is a trend. **For the eight components in this
 register the question does not arise: this is their first assessment, so there is no baseline to
 delta against.**
4. **The myPKI rescore at open item 1 needs a second reader.**

```{=openxml}
<w:p/><w:p/><w:p/>
```

### 4.4 What was verified personally at source

Not the whole population. The following were read at their cited `file:line`, reading the code rather
than the reviewer's summary: the NexusAI fail-open authentication guard; the Vision seed upsert; the
CypherKey EAM subject path and its two correct counterparts; and the product-identity map that
resolves the CypherKey naming collision.

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 5. Assurance Observations

Several design elements hold up under review. They are recorded so that the register is not
discounted wholesale, and they do **not** offset the Critical and High findings.

- **CypherKey's verification core is well built.** Constant-time comparison, consume-on-selection,
 serialisable transactions with `FOR UPDATE SKIP LOCKED` and the reasoning written down, unbiased
 rejection-sampled randomness, four fail-closed startup guards, and device proof with the token
 identifier consumed last.
- **NexusAI's CI secret gate is the most rigorous in the estate.** It carries a custom rule that fires
 on a specific historic secret, plus a **canary step that asserts by rule identifier that the scanner
 can still fire** before a clean result is trusted. An earlier draft wrongly speculated that this was
 an allow-list blinding the scanner; **it is the opposite.**
- **QuickQuote's margin-protection build step holds up under review** *(parked)*. The property it
 carries — that a simple-mode session must never receive the margin tooling or the advanced markup —
 is enforced at build time **and** independently at the server, which is where build-time properties
 usually die. The strip throws on a missing or inverted sentinel pair rather than shipping a partial
 result, and runs a leak check that **refuses to write** if any advanced token or control identifier
 survives into the public HTML. The server then gates the module on both authentication and the
 session's advanced flag, rate-limits the unlock, takes the advanced flag for PDF rendering from the
 session and says why — *"the client decides what state to send, the SERVER decides whether this
 session is entitled"* — and mounts **no static directory at all**, so the private directory is not
 reachable by URL. **Reviewed and clean; nothing filed.**
- **QuickQuote** *(parked)* also shows textbook one-time-password handling, fail-closed boot and
 server-side entitlement decisions.
- **Vision Sales Portal** *(parked)*: **tenant isolation is done properly.** The reviewer went looking
 for the insecure direct object reference and found that every mutator re-derives its authority from
 a scoped read.

---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 6. Keycloak Position

Recorded for completeness, because the Keycloak retirement question spans both registers. Within this
register the position is clean, with one marketing-copy reference.

| Component | Keycloak references |
|---|---|
| Reporting Dashboard (NexusAI) · myPKI · SecurePDF · CryptixWebPortal · HPSM · OneTimePad (CypherKey) | **0** |
| Vision Sales Portal | 1 — marketing copy: *"Keycloakless architecture"* |

The blocking components for the estate-wide Keycloak retirement attestation are all in the companion
HP Authentication Suite register.

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
reason instead.

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
balance.**

**This register's share of the estate**, re-added independently from its own populations:
10 Critical + 27 High + 46 Medium + 33 Low + 16 Informational = **132**. The companion HP
Authentication Suite register carries 18 + 49 + 80 + 40 + 23 = **210**. **132 + 210 = 342**, and the
two registers agree with the estate total band by band.

**Five rows in the combined estate are printed and not counted, and none was deleted:** three marked
withdrawals and two retained split parents. **All five belong to the companion register**, so every
row printed in this register is also counted in it.

---

*End of register. Client Confidential.*
