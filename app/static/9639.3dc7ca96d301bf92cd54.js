/*! For license information please see 9639.3dc7ca96d301bf92cd54.js.LICENSE.txt */
"use strict";(self.webpackChunkUV=self.webpackChunkUV||[]).push([[9639],{2020:(e,t,r)=>{r.r(t),r.d(t,{scopeCss:()=>R});var n="-shadowcsshost",s="-shadowcssslotted",c="-shadowcsscontext",o=")(?:\\(((?:\\([^)(]*\\)|[^)(]*)+?)\\))?([^,{]*)",i=new RegExp("("+n+o,"gim"),a=new RegExp("("+c+o,"gim"),u=new RegExp("("+s+o,"gim"),l=n+"-no-combinator",p=/-shadowcsshost-no-combinator([^\s]*)/,f=[/::shadow/g,/::content/g],h=/-shadowcsshost/gim,g=/:host/gim,m=/::slotted/gim,d=/:host-context/gim,v=/\/\*\s*[\s\S]*?\*\//g,_=/\/\*\s*#\s*source(Mapping)?URL=[\s\S]+?\*\//g,x=/(\s*)([^;\{\}]+?)(\s*)((?:{%BLOCK%}?\s*;?)|(?:\s*;))/g,w=/([{}])/g,b="%BLOCK%",W=function(e,t){var r=O(e),n=0;return r.escapedString.replace(x,(function(){for(var e=[],s=0;s<arguments.length;s++)e[s]=arguments[s];var c=e[2],o="",i=e[4],a="";i&&i.startsWith("{"+b)&&(o=r.blocks[n++],i=i.substring(8),a="{");var u=t({selector:c,content:o});return""+e[1]+u.selector+e[3]+a+u.content+i}))},O=function(e){for(var t=e.split(w),r=[],n=[],s=0,c=[],o=0;o<t.length;o++){var i=t[o];"}"===i&&s--,s>0?c.push(i):(c.length>0&&(n.push(c.join("")),r.push(b),c=[]),r.push(i)),"{"===i&&s++}return c.length>0&&(n.push(c.join("")),r.push(b)),{escapedString:r.join(""),blocks:n}},k=function(e,t,r){return e.replace(t,(function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];if(e[2]){for(var n=e[2].split(","),s=[],c=0;c<n.length;c++){var o=n[c].trim();if(!o)break;s.push(r(l,o,e[3]))}return s.join(",")}return l+e[3]}))},j=function(e,t,r){return e+t.replace(n,"")+r},C=function(e,t,r){return t.indexOf(n)>-1?j(e,t,r):e+t+r+", "+t+" "+e+r},E=function(e,t,r,n,s){return W(e,(function(e){var s=e.selector,c=e.content;return"@"!==e.selector[0]?s=function(e,t,r,n){return e.split(",").map((function(e){return n&&e.indexOf("."+n)>-1?e.trim():function(e,t){return!function(e){return e=e.replace(/\[/g,"\\[").replace(/\]/g,"\\]"),new RegExp("^("+e+")([>\\s~+[.,{:][\\s\\S]*)?$","m")}(t).test(e)}(e,t)?function(e,t,r){t=t.replace(/\[is=([^\]]*)\]/g,(function(e){for(var t=[],r=1;r<arguments.length;r++)t[r-1]=arguments[r];return t[0]}));for(var n,s="."+t,c=function(e){var n=e.trim();if(!n)return"";if(e.indexOf(l)>-1)n=function(e,t,r){if(h.lastIndex=0,h.test(e)){var n="."+r;return e.replace(p,(function(e,t){return t.replace(/([^:]*)(:*)(.*)/,(function(e,t,r,s){return t+n+r+s}))})).replace(h,n+" ")}return t+" "+e}(e,t,r);else{var c=e.replace(h,"");if(c.length>0){var o=c.match(/([^:]*)(:*)(.*)/);o&&(n=o[1]+s+o[2]+o[3])}}return n},o=function(e){var t=[],r=0;return{content:(e=e.replace(/(\[[^\]]*\])/g,(function(e,n){var s="__ph-"+r+"__";return t.push(n),r++,s}))).replace(/(:nth-[-\w]+)(\([^)]+\))/g,(function(e,n,s){var c="__ph-"+r+"__";return t.push(s),r++,n+c})),placeholders:t}}(e),i="",a=0,u=/( |>|\+|~(?!=))\s*/g,f=!((e=o.content).indexOf(l)>-1);null!==(n=u.exec(e));){var g=n[1],m=e.slice(a,n.index).trim();i+=((f=f||m.indexOf(l)>-1)?c(m):m)+" "+g+" ",a=u.lastIndex}var d,v=e.substring(a);return i+=(f=f||v.indexOf(l)>-1)?c(v):v,d=o.placeholders,i.replace(/__ph-(\d+)__/g,(function(e,t){return d[+t]}))}(e,t,r).trim():e.trim()})).join(", ")}(e.selector,t,r,n):(e.selector.startsWith("@media")||e.selector.startsWith("@supports")||e.selector.startsWith("@page")||e.selector.startsWith("@document"))&&(c=E(e.content,t,r,n)),{selector:s.replace(/\s{2,}/g," ").trim(),content:c}}))},R=function(e,t,r){var o=t+"-h",p=t+"-s",h=e.match(_)||[];e=e.replace(v,"");var x=[];if(r){var w=function(e){var t="/*!@___"+x.length+"___*/",r="/*!@"+e.selector+"*/";return x.push({placeholder:t,comment:r}),e.selector=t+e.selector,e};e=W(e,(function(e){return"@"!==e.selector[0]?w(e):e.selector.startsWith("@media")||e.selector.startsWith("@supports")||e.selector.startsWith("@page")||e.selector.startsWith("@document")?(e.content=W(e.content,w),e):e}))}var b=function(e,t,r,o){return e=function(e,t){var r=u;return e.replace(r,(function(){for(var e=[],r=0;r<arguments.length;r++)e[r]=arguments[r];if(e[2]){var n=e[2].trim(),s=e[3];return"."+t+" > "+n+s}return l+e[3]}))}(e=function(e){return k(e,a,C)}(e=function(e){return k(e,i,j)}(e=e.replace(d,c).replace(g,n).replace(m,s))),o),e=function(e){return f.reduce((function(e,t){return e.replace(t," ")}),e)}(e),t&&(e=E(e,t,r,o)),(e=(e=e.replace(/-shadowcsshost-no-combinator/g,"."+r)).replace(/>\s*\*\s+([^{, ]+)/gm," $1 ")).trim()}(e,t,o,p);return e=[b].concat(h).join("\n"),r&&x.forEach((function(t){var r=t.placeholder,n=t.comment;e=e.replace(r,n)})),e}}}]);