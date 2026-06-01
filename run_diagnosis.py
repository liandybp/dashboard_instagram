#!/usr/bin/env python3
import os
os.chdir('/Users/t022458/PycharmProjects/personal/dashboard_instagram')

from src.data.loader import load_account_data_from_zernio_with_fallback

print('\n===== DIAGNÓSTICO DE DATOS ZERNIO =====\n')
data = load_account_data_from_zernio_with_fallback()

print('CONTEOS DE DATOS:')
print(f'  Posts: {len(data.get("posts", []))}')
print(f'  Comments: {len(data.get("comments", []))}')
print(f'  Daily metrics: {len(data.get("daily_metrics", []))}')
print(f'  Best time slots: {len(data.get("best_time_to_post", []))}')
print(f'  Posting frequency: {len(data.get("posting_frequency", []))}')
print(f'  Content decay: {len(data.get("content_decay", []))}')
print(f'  Demographics IG country: {len(data.get("demographics", {}).get("instagram", {}).get("country", []))}')
print(f'  Demographics IG age: {len(data.get("demographics", {}).get("instagram", {}).get("age", []))}')

print(f'\nACCOUNT INFO:')
print(f'  Followers: {data.get("account_snapshot", {}).get("follower_count")}')
print(f'  Posts count: {data.get("account_snapshot", {}).get("posts_count")}')
print(f'  Username: {data.get("account_snapshot", {}).get("username")}')

print('\n===== FIN DIAGNÓSTICO =====\n')

