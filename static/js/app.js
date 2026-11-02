document.addEventListener('mouseup',()=>{const selection=window.getSelection()?.toString().trim();const field=document.querySelector('#selected_text');if(selection&&field)field.value=selection});

const runyankore={
  'Overview':'Obugyenderwaire','Sermon Notebook':'Ekitabo ky’Enyegyesa','+ New sermon':'+ Enyegyesa empya','Sign out':'Ruga','PHANTOMVAULT FAMILY':'Omuryango gwa PhantomVault','SCRIPTURE WORKSPACE':'OMUKORERA GW’EBYAHANDIIKWE','Workspace overview':'Obugyenderwaire bw’omukorera','Make room for the word.':'Kora omwanya gw’ekigambo.','Capture the message, connect the reference, and keep the insight searchable.':'Handika obutumwa, gihuza n’ahandikirwe, kandi obwenge buboneke n’okushaka.','Sermons':'Enyegyesa','private workspaces':'abakorerwa ab’ekyama','Sources':'Enshoko','provider records':'amakuru g’enkora','Text status':'Embeera y’ebigambo','Reference':'Ahahandikirwe','rights-safe prototype':'eky’okugezaho ekirikuteekateeka obushoboorozi','RECENT NOTES':'AMAKURU G’AHERU','Latest sermon workspaces':'Abakorerwa b’enyegyesa abaheruka','Open notebook →':'Zingura ekitabo →','Your notebook is empty.':'Ekitabo kyawe tikirimu kintu.','Start with the next sermon, study session, or teaching idea.':'Tandika n’enyegyesa, okwega, nari ekirowoozo ky’okwegyesa ekirikurataho.','Sermon notebook':'Ekitabo ky’enyegyesa','Search title, content or location':'Shaka omutwe, amakuru nari omwanya','Speaker':'Orikugamba','Topic':'Omubazi','Filter':'Tunga','No sermons found.':'Tihariho nyegyesa zabonsekire.','New sermon':'Enyegyesa empya','Edit sermon':'Hindura enyegyesa','Title':'Omutwe','Date and time':'Eizooba n’obwire','Church / event / location':'Ekanisa / omukoro / omwanya','Notes':'Amakuru','Save sermon':'Bika enyegyesa','Cancel':'Rugamu','SERMON NOTES':'AMAKURU G’ENYEGYESA','SCRIPTURE REFERENCES':'AHAHANDIKIRWE BY’EBYAHANDIIKWE','Save reference':'Bika ahahandikirwe','HIGHLIGHTS':'EBYAYAKIIRWE','Save highlight':'Bika ekyayakiirwe','Comment':'Kugamba','MATCH REVIEW':'OKUSHARURA AHANDIKIRWE','Save match record':'Bika amakuru g’okusharura','Delete':'Siba','Edit fields':'Hindura ebyandikirwe','Exact quotation — verify':'Ekihandiiko kimwe — kihakanye','Partial / likely — verify':'Ekihandiiko ekishushana — kihakanye','Related suggestion — not a quotation':'Ekihandiiko ekishushana — tikiri kihandiiko kyonyini','Unverified':'Tikihakaniibwe','Study with a memory.':'Ega n’obwima.','Sign in':'Yingira','Email':'Eposita','Password':'Enshonga y’ekyama','Bible text is not bundled until an authorised source is configured.':'Ebigambo bya Baibuli tibirimu okuhisya ahabumbwa enshoko erikikirizibwa.'
};
const englishButton='Runyankore';
function translateInterface(enabled){
  document.documentElement.lang=enabled?'nyn':'en';
  document.querySelectorAll('body *').forEach(el=>{
    if(el.children.length || el.matches('input,textarea,select,option,.note-content,.list-row strong,.list-row small,.highlight strong,.highlight p')) return;
    if(!el.dataset.originalText) el.dataset.originalText=el.textContent;
    const original=el.dataset.originalText.trim();
    if(!original) return;
    el.textContent=enabled && runyankore[original] ? runyankore[original] : original;
  });
  document.querySelectorAll('input,textarea').forEach(el=>{
    if(!el.dataset.originalPlaceholder) el.dataset.originalPlaceholder=el.placeholder||'';
    const p=el.dataset.originalPlaceholder;
    if(enabled && runyankore[p]) el.placeholder=runyankore[p]; else el.placeholder=p;
  });
  const toggle=document.querySelector('#language-toggle');
  if(toggle){toggle.textContent=enabled?'English':englishButton;toggle.setAttribute('aria-pressed',String(enabled));}
  localStorage.setItem('scriptureStudioLanguage',enabled?'runyankore':'english');
}
document.addEventListener('DOMContentLoaded',()=>{const toggle=document.querySelector('#language-toggle');const enabled=localStorage.getItem('scriptureStudioLanguage')==='runyankore';translateInterface(enabled);if(toggle)toggle.addEventListener('click',()=>translateInterface(localStorage.getItem('scriptureStudioLanguage')!=='runyankore'));});