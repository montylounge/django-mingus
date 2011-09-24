/**
 * $Id: editor_plugin_src.js 264 2007-04-26 20:53:09Z spocke $
 *
 * @author Moxiecode
 * @copyright Copyright � 2004-2008, Moxiecode Systems AB, All rights reserved.
 */

(function() {
	var Event = tinymce.dom.Event, grep = tinymce.grep, each = tinymce.each, inArray = tinymce.inArray;

	function isEmpty(d, e, f) {
		var w, n;

		w = d.createTreeWalker(e, NodeFilter.SHOW_ALL, null, false);
		while (n = w.nextNode()) {
			// Filter func
			if (f) {
				if (!f(n))
					return false;
			}

			// Non whitespace text node
			if (n.nodeType == 3 && n.nodeValue && /[^\s\u00a0]+/.test(n.nodeValue))
				return false;

			// Is non text element byt still content
			if (n.nodeType == 1 && /^(HR|IMG|TABLE)$/.test(n.nodeName))
				return false;
		}

		return true;
	};

	tinymce.create('tinymce.plugins.Safari', {
		init : function(ed) {
			var t = this, dom;

			// Ignore on non webkit
			if (!tinymce.isWebKit)
				return;

			t.editor = ed;
			t.webKitFontSizes = ['x-small', 'small', 'medium', 'large', 'x-large', 'xx-large', '-webkit-xxx-large'];
			t.namedFontSizes = ['xx-small', 'x-small','small','medium','large','x-large', 'xx-large'];

			// Safari CreateLink command will not work correctly on images that is aligned
			ed.addCommand('CreateLink', function(u, v) {
				var n = ed.selection.getNode(), dom = ed.dom, a;

				if (n && (/^(left|right)$/i.test(dom.getStyle(n, 'float', 1)) || /^(left|right)$/i.test(dom.getAttrib(n, 'align')))) {
					a = dom.create('a', {href : v}, n.cloneNode());
					n.parentNode.replaceChild(a, n);
					ed.selection.select(a);
				} else
					ed.getDoc().execCommand("CreateLink", false, v);
			});

/*
			// WebKit generates spans out of thin air this patch used to remove them but it will also remove styles we want so it's disabled for now
			ed.onPaste.add(function(ed, e) {
				function removeStyles(e) {
					e = e.target;

					if (e.nodeType == 1) {
						e.style.cssText = '';

						each(ed.dom.select('*', e), function(e) {
							e.style.cssText = '';
						});
					}
				};

				Event.add(ed.getDoc(), 'DOMNodeInserted', removeStyles);

				window.setTimeout(function() {
					Event.remove(ed.getDoc(), 'DOMNodeInserted', removeStyles);
				}, 0);
			});
*/
			ed.onKeyUp.add(function(ed, e) {
				var h, b, r, n, s;

				// If backspace or delete key
				if (e.keyCode == 46 || e.keyCode == 8) {
					b = ed.getBody();
					h = b.innerHTML;
					s = ed.selection;

					// If there is no text content or images or hr elements then remove everything
					if (b.childNodes.length == 1 && !/<(img|hr)/.test(h) && tinymce.trim(h.replace(/<[^>]+>/g, '')).length == 0) {
						// Inject paragrah and bogus br
						ed.setContent('<p><br mce_bogus="1" /></p>', {format : 'raw'});

						// Move caret before bogus br
						n = b.firstChild;
						r = s.getRng();
						r.setStart(n, 0);
						r.setEnd(n, 0);
						s.setRng(r);
					}
				}
			});

			// Workaround for FormatBlock bug, http://bugs.webkit.org/show_bug.cgi?id=16004
			ed.addCommand('FormatBlock', function(u, v) {
				var dom = ed.dom, e = dom.getParent(ed.selection.getNode(), dom.isBlock);

				if (e)
					dom.replace(dom.create(v), e, 1);
				else
					ed.getDoc().execCommand("FormatBlock", false, v);
			});

			// Workaround for InsertHTML bug, http://bugs.webkit.org/show_bug.cgi?id=16382
			ed.addCommand('mceInsertContent', function(u, v) {
				ed.getDoc().execCommand("InsertText", false, 'mce_marker');
				ed.getBody().innerHTML = ed.getBody().innerHTML.replace(/mce_marker/g, ed.dom.processHTML(v) + '<span id="_mce_tmp">XX</span>');
				ed.selection.select(ed.dom.get('_mce_tmp'));
				ed.getDoc().execCommand("Delete", false, ' ');
			});
	
	/*		ed.onKeyDown.add(function(ed, e) {
				// Ctrl+A select all will fail on WebKit since if you paste the contents you selected it will produce a odd div wrapper
				if ((e.ctrlKey || e.metaKey) && e.keyCode == 65) {
					ed.selection.select(ed.getBody(), 1);
					return Event.cancel(e);
				}
			});*/

			ed.onKeyPress.add(function(ed, e) {
				var se, li, lic, r1, r2, n, sel, doc, be, af, pa;

				if (e.keyCode == 13) {
					sel = ed.selection;
					se = sel.getNode();

					// Workaround for missing shift+enter support, http://bugs.webkit.org/show_bug.cgi?id=16973
					if (e.shiftKey || ed.settings.force_br_newlines && se.nodeName != 'LI') {
						t._insertBR(ed);
						Event.cancel(e);
					}

					// Workaround for DIV elements produced by Safari
					if (li = dom.getParent(se, 'LI')) {
						lic = dom.getParent(li, 'OL,UL');
						doc = ed.getDoc();

						pa = dom.create('p');
						dom.add(pa, 'br', {mce_bogus : "1"});

						if (isEmpty(doc, li)) {
							// If list in list then use browser default behavior
							if (n = dom.getParent(lic.parentNode, 'LI,OL,UL'))
								return;

							n = dom.getParent(lic, 'p,h1,h2,h3,h4,h5,h6,div') || lic;

							// Create range from the start of block element to the list item
							r1 = doc.createRange();
							r1.setStartBefore(n);
							r1.setEndBefore(li);

							// Create range after the list to the end of block element
							r2 = doc.createRange();
							r2.setStartAfter(li);
							r2.setEndAfter(n);

							be = r1.cloneContents();
							af = r2.cloneContents();

							if (!isEmpty(doc, af))
								dom.insertAfter(af, n);

							dom.insertAfter(pa, n);

							if (!isEmpty(doc, be))
								dom.insertAfter(be, n);

							dom.remove(n);

							n = pa.firstChild;
							r1 = doc.createRange();
							r1.setStartBefore(n);
							r1.setEndBefore(n);
							sel.setRng(r1);

							return Event.cancel(e);
						}
					}
				}
			});

			// Safari doesn't place lists outside block elements
			ed.onExecCommand.add(function(ed, cmd) {
				var sel, dom, bl, bm;

				if (cmd == 'InsertUnorderedList' || cmd == 'InsertOrderedList') {
					sel = ed.selection;
					dom = ed.dom;

					if (bl = dom.getParent(sel.getNode(), function(n) {return /^(H[1-6]|P|ADDRESS|PRE)$/.test(n.nodeName);})) {
						bm = sel.getBookmark();
						dom.remove(bl, 1);
						sel.moveToBookmark(bm);
					}
				}
			});

			// Workaround for bug, http://bugs.webkit.org/show_bug.cgi?id=12250
			ed.onClick.add(function(ed, e) {
				e = e.target;

				if (e.nodeName == 'IMG') {
					t.selElm = e;
					ed.selection.select(e);
				} else
					t.selElm = null;
			});

			ed.onInit.add(function() {
				t._fixWebKitSpans();
			});

			ed.onSetContent.add(function() {
				dom = ed.dom;

				// Convert strong,b,em,u,strike to spans
				each(['strong','b','em','u','strike','sub','sup','a'], function(v) {
					each(grep(dom.select(v)).reverse(), function(n) {
						var nn = n.nodeName.toLowerCase(), st;

						// Convert anchors into images
						if (nn == 'a') {
							if (n.name)
								dom.replace(dom.create('img', {mce_name : 'a', name : n.name, 'class' : 'mceItemAnchor'}), n);

							return;
						}

						switch (nn) {
							case 'b':
							case 'strong':
								if (nn == 'b')
									nn = 'strong';

								st = 'font-weight: bold;';
								break;

							case 'em':
								st = 'font-style: italic;';
								break;

							case 'u':
								st = 'text-decoration: underline;';
								break;

							case 'sub':
								st = 'vertical-align: sub;';
								break;

							case 'sup':
								st = 'vertical-align: super;';
								break;

							case 'strike':
								st = 'text-decoration: line-through;';
								break;
						}

						dom.replace(dom.create('span', {mce_name : nn, style : st, 'class' : 'Apple-style-span'}), n, 1);
					});
				});
			});

			ed.onPreProcess.add(function(ed, o) {
				dom = ed.dom;

				each(grep(o.node.getElementsByTagName('span')).reverse(), function(n) {
					var v, bg;

					if (o.get) {
						if (dom.hasClass(n, 'Apple-style-span')) {
							bg = n.style.backgroundColor;

							switch (dom.getAttrib(n, 'mce_name')) {
								case 'font':
									if (!ed.settings.convert_fonts_to_spans)
										dom.setAttrib(n, 'style', '');
									break;

								case 'strong':
								case 'em':
								case 'sub':
								case 'sup':
									dom.setAttrib(n, 'style', '');
									break;

								case 'strike':
								case 'u':
									if (!ed.settings.inline_styles)
										dom.setAttrib(n, 'style', '');
									else
										dom.setAttrib(n, 'mce_name', '');

									break;

								default:
									if (!ed.settings.inline_styles)
										dom.setAttrib(n, 'style', '');
							}


							if (bg)
								n.style.backgroundColor = bg;
						}
					}

					if (dom.hasClass(n, 'mceItemRemoved'))
						dom.remove(n, 1);
				});
			});

			ed.onPostProcess.add(function(ed, o) {
				// Safari adds BR at end of all block elements
				o.content = o.content.replace(/<br \/><\/(h[1-6]|div|p|address|pre)>/g, '</$1>');

				// Safari adds id="undefined" to HR elements
				o.content = o.content.replace(/ id=\"undefined\"/g, '');
			});
		},

		getInfo : function() {
			return {
				longname : 'Safari compatibility',
				author : 'Moxiecode Systems AB',
				authorurl : 'http://tinymce.moxiecode.com',
				infourl : 'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/safari',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		},

		// Internal methods

		_fixWebKitSpans : function() {
			var t = this, ed = t.editor;

			// Use mutator events on new WebKit
			Event.add(ed.getDoc(), 'DOMNodeInserted', function(e) {
				e = e.target;

				if (e && e.nodeType == 1)
					t._fixAppleSpan(e);
			});
		},

		_fixAppleSpan : function(e) {
			var ed = this.editor, dom = ed.dom, fz = this.webKitFontSizes, fzn = this.namedFontSizes, s = ed.settings, st, p;

			if (dom.getAttrib(e, 'mce_fixed'))
				return;

			// Handle Apple style spans
			if (e.nodeName == 'SPAN' && e.className == 'Apple-style-span') {
				st = e.style;

				if (!s.convert_fonts_to_spans) {
					if (st.fontSize) {
						dom.setAttrib(e, 'mce_name', 'font');
						dom.setAttrib(e, 'size', inArray(fz, st.fontSize) + 1);
					}

					if (st.fontFamily) {
						dom.setAttrib(e, 'mce_name', 'font');
						dom.setAttrib(e, 'face', st.fontFamily);
					}

					if (st.color) {
						dom.setAttrib(e, 'mce_name', 'font');
						dom.setAttrib(e, 'color', dom.toHex(st.color));
					}

					if (st.backgroundColor) {
						dom.setAttrib(e, 'mce_name', 'font');
						dom.setStyle(e, 'background-color', st.backgroundColor);
					}
				} else {
					if (st.fontSize)
						dom.setStyle(e, 'fontSize', fzn[inArray(fz, st.fontSize)]);
				}

				if (st.fontWeight == 'bold')
					dom.setAttrib(e, 'mce_name', 'strong');

				if (st.fontStyle == 'italic')
					dom.setAttrib(e, 'mce_name', 'em');

				if (st.textDecoration == 'underline')
					dom.setAttrib(e, 'mce_name', 'u');

				if (st.textDecoration == 'line-through')
					dom.setAttrib(e, 'mce_name', 'strike');

				if (st.verticalAlign == 'super')
					dom.setAttrib(e, 'mce_name', 'sup');

				if (st.verticalAlign == 'sub')
					dom.setAttrib(e, 'mce_name', 'sub');

				dom.setAttrib(e, 'mce_fixed', '1');
			}
		},

		_insertBR : function(ed) {
			var dom = ed.dom, s = ed.selection, r = s.getRng(), br;

			// Insert BR element
			r.insertNode(br = dom.create('br'));

			// Place caret after BR
			r.setStartAfter(br);
			r.setEndAfter(br);
			s.setRng(r);

			// Could not place caret after BR then insert an nbsp entity and move the caret
			if (s.getSel().focusNode == br.previousSibling) {
				s.select(dom.insertAfter(dom.doc.createTextNode('\u00a0'), br));
				s.collapse(1);
			}

			// Scroll to new position, scrollIntoView can't be used due to bug: http://bugs.webkit.org/show_bug.cgi?id=16117
			ed.getWin().scrollTo(0, dom.getPos(s.getRng().startContainer).y);
		}
	});

	// Register plugin
	tinymce.PluginManager.add('safari', tinymce.plugins.Safari);
})();

