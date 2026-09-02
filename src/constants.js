/** @typedef {'serif'|'sans-serif'|'display'|'monospace'|'handwritten'} Category */
/** @typedef {'cozy'|'bold'|'elegant'|'playful'|'minimal'|'retro'} Mood */
/** @typedef {{id:string,fontName:string,category:Category,spotted:string,sample:string,mood:Mood,dateSaved:string}} FontEntry */
export const CATEGORIES=['serif','sans-serif','display','monospace','handwritten'];
export const MOODS=['cozy','bold','elegant','playful','minimal','retro'];
export const STORAGE_KEY='font-crush.entries.v1';
