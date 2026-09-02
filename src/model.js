import{CATEGORIES,MOODS}from'./constants.js';
const clean=value=>String(value??'').trim();
/** Validate and normalize untrusted form data. @param {Record<string,unknown>} raw */
export function validateEntry(raw){
 const value={fontName:clean(raw.fontName),category:clean(raw.category),spotted:clean(raw.spotted),sample:clean(raw.sample),mood:clean(raw.mood)};
 const errors={};
 if(!value.fontName)errors.fontName='Name the font you want to remember.';else if(value.fontName.length>80)errors.fontName='Use 80 characters or fewer.';
 if(!value.spotted)errors.spotted='Add where you spotted it.';else if(value.spotted.length>100)errors.spotted='Use 100 characters or fewer.';
 if(!value.sample)errors.sample='Add a sentence to preview.';else if(value.sample.length>180)errors.sample='Use 180 characters or fewer.';
 if(!CATEGORIES.includes(value.category))errors.category='Choose a valid category.';
 if(!MOODS.includes(value.mood))errors.mood='Choose a valid mood.';
 return{ok:Object.keys(errors).length===0,value,errors};
}
/** @param {unknown} value @returns {value is import('./constants.js').FontEntry} */
export function isEntry(value){if(!value||typeof value!=='object')return false;const checked=validateEntry(value);return checked.ok&&value.fontName===checked.value.fontName&&value.spotted===checked.value.spotted&&value.sample===checked.value.sample&&/^[\w-]{1,100}$/u.test(value.id)&&typeof value.dateSaved==='string'&&!Number.isNaN(Date.parse(value.dateSaved))}
/** @param {import('./constants.js').FontEntry[]} entries @param {string} category @param {string} mood */
export function filterEntries(entries,category,mood){return entries.filter(item=>(!category||item.category===category)&&(!mood||item.mood===mood))}
/** Parse and validate a complete JSON backup. @param {string} raw */
export function parseImport(raw){try{const data=JSON.parse(raw);if(!Array.isArray(data))return{ok:false,error:'The backup must contain a list of font entries.'};if(!data.every(isEntry))return{ok:false,error:'The backup contains an invalid or incomplete font entry.'};if(new Set(data.map(x=>x.id)).size!==data.length)return{ok:false,error:'The backup contains duplicate entry IDs.'};return{ok:true,entries:data}}catch{return{ok:false,error:'That file is not valid JSON.'}}}
