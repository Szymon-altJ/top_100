# BillboardTop100

Projekt "top100" to moja własna hobbistyczna praca.

Po uruchomieniu program za pomocą web scrapingu pobiera ze strony Billboard Top 100 - 100 najczęsciej słuchanych danego dnia utworów (na platformie Spotify). 
Obok autorów i nazwy utworu, program stara się też dobrać gatunek muzyki jaki tworzy wykonawca, wyszukując tą informacje na stronie wikipedia autora, lub z dostarczonej bazy danych.

# Wykorzystane Biblioteki
-requests
-beautifulsoup4
-pandas
-wikipedia
-wptools
-re


# Dokładność
Aktualnie na dzień 08.08.2025 program jest w stanie dopasować (bez cache) ~45% gatunków, odpowiadających wykonawcą w top100.

