(self.webpackChunkUV=self.webpackChunkUV||[]).push([[2898],{2898:()=>{var t=function(){this.start=0,this.end=0,this.previous=null,this.parent=null,this.rules=null,this.parsedCssText="",this.cssText="",this.atRule=!1,this.type=0,this.keyframesName="",this.selector="",this.parsedSelector=""};function e(e){return r(function(e){var r=new t;r.start=0,r.end=e.length;for(var n=r,a=0,o=e.length;a<o;a++)if(e[a]===s){n.rules||(n.rules=[]);var u=n,l=u.rules[u.rules.length-1]||null;(n=new t).start=a+1,n.parent=u,n.previous=l,u.rules.push(n)}else e[a]===i&&(n.end=a+1,n=n.parent||r);return r}(e=e.replace(a.comments,"").replace(a.port,"")),e)}function r(t,e){var s=e.substring(t.start,t.end-1);if(t.parsedCssText=t.cssText=s.trim(),t.parent){var i=t.previous?t.previous.end:t.parent.start;s=function(t){return t.replace(/\\([0-9a-f]{1,6})\s/gi,(function(){for(var t=arguments[1],e=6-t.length;e--;)t="0"+t;return"\\"+t}))}(s=e.substring(i,t.start-1)),s=(s=s.replace(a.multipleSpaces," ")).substring(s.lastIndexOf(";")+1);var c=t.parsedSelector=t.selector=s.trim();t.atRule=0===c.indexOf(l),t.atRule?0===c.indexOf(u)?t.type=n.MEDIA_RULE:c.match(a.keyframesRule)&&(t.type=n.KEYFRAMES_RULE,t.keyframesName=t.selector.split(a.multipleSpaces).pop()):0===c.indexOf(o)?t.type=n.MIXIN_RULE:t.type=n.STYLE_RULE}var p=t.rules;if(p)for(var f=0,h=p.length,v=void 0;f<h&&(v=p[f]);f++)r(v,e);return t}var n={STYLE_RULE:1,KEYFRAMES_RULE:7,MEDIA_RULE:4,MIXIN_RULE:1e3},s="{",i="}",a={comments:/\/\*[^*]*\*+([^/*][^*]*\*+)*\//gim,port:/@import[^;]*;/gim,customProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?(?:[;\n]|$)/gim,mixinProp:/(?:^[^;\-\s}]+)?--[^;{}]*?:[^{};]*?{[^}]*?}(?:[;\n]|$)?/gim,mixinApply:/@apply\s*\(?[^);]*\)?\s*(?:[;\n]|$)?/gim,varApply:/[^;:]*?:[^;]*?var\([^;]*\)(?:[;\n]|$)?/gim,keyframesRule:/^@[^\s]*keyframes/,multipleSpaces:/\s+/g},o="--",u="@media",l="@";function c(t,e,r){t.lastIndex=0;var n=e.substring(r).match(t);if(n){var s=r+n.index;return{start:s,end:s+n[0].length}}return null}var p=/\bvar\(/,f=/\B--[\w-]+\s*:/,h=/\/\*[^*]*\*+([^/*][^*]*\*+)*\//gim,v=/^[\t ]+\n/gm;function m(t,e,r){var n=function(t,e){var r=c(p,t,e);if(!r)return null;var n=function(t,e){for(var r=0,n=e;n<t.length;n++){var s=t[n];if("("===s)r++;else if(")"===s&&--r<=0)return n+1}return n}(t,r.start),s=t.substring(r.end,n-1).split(","),i=s[0],a=s.slice(1);return{start:r.start,end:n,propName:i.trim(),fallback:a.length>0?a.join(",").trim():void 0}}(t,r);if(!n)return e.push(t.substring(r,t.length)),t.length;var s=n.propName,i=null!=n.fallback?y(n.fallback):void 0;return e.push(t.substring(r,n.start),(function(t){return function(t,e,r){return t[e]?t[e]:r?d(r,t):""}(t,s,i)})),n.end}function d(t,e){for(var r="",n=0;n<t.length;n++){var s=t[n];r+="string"==typeof s?s:s(e)}return r}function g(t,e){for(var r=!1,n=!1,s=e;s<t.length;s++){var i=t[s];if(r)n&&'"'===i&&(r=!1),n||"'"!==i||(r=!1);else if('"'===i)r=!0,n=!0;else if("'"===i)r=!0,n=!1;else{if(";"===i)return s+1;if("}"===i)return s}}return s}function y(t){var e=0;t=function(t){for(var e="",r=0;;){var n=c(f,t,r),s=n?n.start:t.length;if(e+=t.substring(r,s),!n)break;r=g(t,s)}return e}(t=t.replace(h,"")).replace(v,"");for(var r=[];e<t.length;)e=m(t,r,e);return r}function S(t){var e={};t.forEach((function(t){t.declarations.forEach((function(t){e[t.prop]=t.value}))}));for(var r={},n=Object.entries(e),s=function(t){var e=!1;if(n.forEach((function(t){var n=t[0],s=d(t[1],r);s!==r[n]&&(r[n]=s,e=!0)})),!e)return"break"},i=0;i<10&&"break"!==s();i++);return r}function E(t,e){if(void 0===e&&(e=0),!t.rules)return[];var r=[];return t.rules.filter((function(t){return t.type===n.STYLE_RULE})).forEach((function(t){var n=function(t){for(var e,r=[];e=M.exec(t.trim());){var n=L(e[2]),s=n.value,i=n.important;r.push({prop:e[1].trim(),value:y(s),important:i})}return r}(t.cssText);n.length>0&&t.parsedSelector.split(",").forEach((function(t){t=t.trim(),r.push({selector:t,declarations:n,specificity:1,nu:e})})),e++})),r}var b="!important",M=/(?:^|[;\s{]\s*)(--[\w-]*?)\s*:\s*(?:((?:'(?:\\'|.)*?'|"(?:\\"|.)*?"|\([^)]*?\)|[^};{])+)|\{([^}]*)\}(?:(?=[;\s}])|$))/gm;function L(t){var e=(t=t.replace(/\s+/gim," ").trim()).endsWith(b);return e&&(t=t.substr(0,t.length-b.length).trim()),{value:t,important:e}}function k(t){var e=[];return t.forEach((function(t){e.push.apply(e,t.selectors)})),e}function w(t){var r=e(t),n=y(t);return{original:t,template:n,selectors:E(r),usesCssVars:n.length>1}}function x(t,e){var r=w(e.innerHTML);r.styleEl=e,t.push(r)}function R(t,e,r){var n,s;return n="\\."+e,s="."+r,t.replace(new RegExp(n,"g"),s)}function T(t,e,r){var n=r.href;return fetch(n).then((function(t){return t.text()})).then((function(s){if(((a=s).indexOf("var(")>-1||_.test(a))&&r.parentNode){(function(t){return I.lastIndex=0,I.test(t)})(s)&&(s=function(t,e){var r=e.replace(/[^/]*$/,"");return t.replace(I,(function(t,e){var n=r+e;return t.replace(e,n)}))}(s,n));var i=t.createElement("style");i.setAttribute("data-styles",""),i.innerHTML=s,x(e,i),r.parentNode.insertBefore(i,r),r.remove()}var a})).catch((function(t){console.error(t)}))}var _=/[\s;{]--[-a-zA-Z0-9]+\s*:/m,I=/url[\s]*\([\s]*['"]?(?![http|/])([^\'\"\)]*)[\s]*['"]?\)[\s]*/gim,C=function(){function t(t,e){this.win=t,this.doc=e,this.count=0,this.hostStyleMap=new WeakMap,this.hostScopeMap=new WeakMap,this.globalScopes=[],this.scopesMap=new Map}return t.prototype.initShim=function(){var t=this;return new Promise((function(e){t.win.requestAnimationFrame((function(){var r,n;(r=t.doc,n=t.globalScopes,function(t,e){for(var r=t.querySelectorAll("style:not([data-styles])"),n=0;n<r.length;n++)x(e,r[n])}(r,n),function(t,e){for(var r=[],n=t.querySelectorAll('link[rel="stylesheet"][href]'),s=0;s<n.length;s++)r.push(T(t,e,n[s]));return Promise.all(r)}(r,n)).then((function(){return e()}))}))}))},t.prototype.addLink=function(t){var e=this;return T(this.doc,this.globalScopes,t).then((function(){e.updateGlobal()}))},t.prototype.addGlobalStyle=function(t){x(this.globalScopes,t),this.updateGlobal()},t.prototype.createHostStyle=function(t,e,r,n){if(this.hostScopeMap.has(t))throw new Error("host style already created");var s,i,a,o,u=this.registerHostTemplate(r,e,n),l=this.doc.createElement("style");return u.usesCssVars?n?(l["s-sc"]=e=u.scopeId+"-"+this.count,l.innerHTML="/*needs update*/",this.hostStyleMap.set(t,l),this.hostScopeMap.set(t,(i=e,a=(s=u).template.map((function(t){return"string"==typeof t?R(t,s.scopeId,i):t})),o=s.selectors.map((function(t){return Object.assign({},t,{selector:R(t.selector,s.scopeId,i)})})),Object.assign({},s,{template:a,selectors:o,scopeId:i}))),this.count++):(u.styleEl=l,u.usesCssVars||(l.innerHTML=d(u.template,{})),this.globalScopes.push(u),this.updateGlobal(),this.hostScopeMap.set(t,u)):l.innerHTML=r,l},t.prototype.removeHost=function(t){var e=this.hostStyleMap.get(t);e&&e.remove(),this.hostStyleMap.delete(t),this.hostScopeMap.delete(t)},t.prototype.updateHost=function(t){var e=this.hostScopeMap.get(t);if(e&&e.usesCssVars&&e.isScoped){var r=this.hostStyleMap.get(t);if(r){var n=function(t,e,r){var n,s=[],i=function(t,e){for(var r=[];e;){var n=t.get(e);n&&r.push(n),e=e.parentElement}return r}(e,t);return r.forEach((function(t){return s.push(t)})),i.forEach((function(t){return s.push(t)})),(n=k(s).filter((function(e){return function(t,e){return":root"===e||"html"===e||t.matches(e)}(t,e.selector)}))).sort((function(t,e){return t.specificity===e.specificity?t.nu-e.nu:t.specificity-e.specificity})),n}(t,this.hostScopeMap,this.globalScopes),s=S(n);r.innerHTML=d(e.template,s)}}},t.prototype.updateGlobal=function(){var t,e;t=this.globalScopes,e=S(k(t)),t.forEach((function(t){t.usesCssVars&&(t.styleEl.innerHTML=d(t.template,e))}))},t.prototype.registerHostTemplate=function(t,e,r){var n=this.scopesMap.get(e);return n||((n=w(t)).scopeId=e,n.isScoped=r,this.scopesMap.set(e,n)),n},t}(),H=window;H.__stencil_cssshim||H.CSS&&H.CSS.supports&&H.CSS.supports("color","var(--c)")||(H.__stencil_cssshim=new C(H,document))}}]);