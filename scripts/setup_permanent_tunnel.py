#!/usr/bin/env python3
"""
永続的トンネル設定システム
ngrok代替案とセットアップ自動化

Author: Claude Code
Date: 2025-08-10  
"""

import subprocess
import json
import os
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TunnelManager:
    """トンネル管理システム"""
    
    def __init__(self):
        self.config_file = Path('/Users/skem/Himawari/SEO_AUTO_BLOG_PROJECT/config/tunnel_config.json')
        self.local_port = 8080
        
    def setup_cloudflare_tunnel(self):
        """Cloudflare Tunnel設定（無料・永続的）"""
        print("🌐 Cloudflare Tunnel設定中...")
        
        try:
            # cloudflared インストール確認
            result = subprocess.run(['cloudflared', '--version'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print("📦 cloudflared installing...")
                subprocess.run(['brew', 'install', 'cloudflared'], check=True)
            
            print("✅ cloudflared ready")
            
            # トンネル作成
            tunnel_name = "himawari-error-monitor"
            
            # 既存トンネル削除（あれば）
            subprocess.run(['cloudflared', 'tunnel', 'delete', tunnel_name], 
                          capture_output=True)
            
            # 新規トンネル作成
            create_result = subprocess.run([
                'cloudflared', 'tunnel', 'create', tunnel_name
            ], capture_output=True, text=True, check=True)
            
            print(f"✅ トンネル作成完了: {tunnel_name}")
            
            # 設定ファイル作成
            config_content = f"""
tunnel: {tunnel_name}
credentials-file: /Users/{os.getenv('USER')}/.cloudflared/{tunnel_name}.json

ingress:
  - hostname: {tunnel_name}.trycloudflare.com
    service: http://localhost:{self.local_port}
  - service: http_status:404
"""
            
            config_dir = Path(f"/Users/{os.getenv('USER')}/.cloudflared")
            config_dir.mkdir(exist_ok=True)
            
            config_path = config_dir / "config.yml"
            with open(config_path, 'w') as f:
                f.write(config_content)
            
            print("✅ Cloudflare Tunnel設定完了")
            print(f"🌐 URL: https://{tunnel_name}.trycloudflare.com")
            
            # 設定保存
            self.save_tunnel_config({
                'type': 'cloudflare',
                'name': tunnel_name,
                'url': f"https://{tunnel_name}.trycloudflare.com",
                'local_port': self.local_port
            })
            
            return f"https://{tunnel_name}.trycloudflare.com"
            
        except Exception as e:
            print(f"❌ Cloudflare Tunnel設定エラー: {e}")
            return None
    
    def setup_serveo_tunnel(self):
        """Serveo設定（簡単・無料）"""
        print("🚇 Serveo Tunnel設定中...")
        
        try:
            # SSH経由でトンネル作成
            tunnel_name = "himawari-errors"
            serveo_url = f"https://{tunnel_name}.serveo.net"
            
            print(f"🌐 Serveo URL: {serveo_url}")
            
            # バックグラウンドでトンネル開始
            subprocess.Popen([
                'ssh', '-R', f'{tunnel_name}:80:localhost:{self.local_port}',
                'serveo.net'
            ])
            
            time.sleep(3)  # 接続待ち
            
            print("✅ Serveo Tunnel設定完了")
            
            # 設定保存
            self.save_tunnel_config({
                'type': 'serveo',
                'name': tunnel_name,
                'url': serveo_url,
                'local_port': self.local_port
            })
            
            return serveo_url
            
        except Exception as e:
            print(f"❌ Serveo設定エラー: {e}")
            return None
    
    def setup_localtunnel(self):
        """LocalTunnel設定（npm経由）"""
        print("🔧 LocalTunnel設定中...")
        
        try:
            # localtunnel インストール確認
            result = subprocess.run(['lt', '--version'], 
                                  capture_output=True)
            
            if result.returncode != 0:
                print("📦 localtunnel installing...")
                subprocess.run(['npm', 'install', '-g', 'localtunnel'], check=True)
            
            # カスタムサブドメイン指定
            subdomain = "himawari-error-monitor"
            
            # トンネル開始
            process = subprocess.Popen([
                'lt', '--port', str(self.local_port), 
                '--subdomain', subdomain
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            time.sleep(3)  # 接続待ち
            
            tunnel_url = f"https://{subdomain}.loca.lt"
            
            print(f"🌐 LocalTunnel URL: {tunnel_url}")
            print("✅ LocalTunnel設定完了")
            
            # 設定保存
            self.save_tunnel_config({
                'type': 'localtunnel',
                'subdomain': subdomain,
                'url': tunnel_url,
                'local_port': self.local_port,
                'process_id': process.pid
            })
            
            return tunnel_url
            
        except Exception as e:
            print(f"❌ LocalTunnel設定エラー: {e}")
            return None
    
    def save_tunnel_config(self, config):
        """トンネル設定保存"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"📋 設定保存: {self.config_file}")

def update_webhook_urls(new_url):
    """Webhook URL更新"""
    print(f"🔄 Webhook URL更新中: {new_url}")
    
    # GitHub Webhook更新
    try:
        subprocess.run([
            'gh', 'api', 'repos/satoshi-kemmotsu/blog/hooks',
            '--method', 'PATCH',
            '--field', f'config.url={new_url}/github-webhook'
        ], check=True)
        print("✅ GitHub Webhook更新完了")
        
    except Exception as e:
        print(f"❌ GitHub Webhook更新エラー: {e}")
    
    # Netlify Webhook（手動設定の案内）
    print(f"""
📋 Netlify Webhook手動更新が必要:
1. https://app.netlify.com/projects/neon-biscochitos-8dd468
2. Site settings → Build & deploy → Deploy notifications
3. URL更新: {new_url}/netlify-webhook
""")

def main():
    """メイン実行"""
    manager = TunnelManager()
    
    print("🚀 永続的トンネル設定開始")
    print("=" * 40)
    
    # 優先順位順に試行
    tunnel_services = [
        ("Cloudflare Tunnel", manager.setup_cloudflare_tunnel),
        ("LocalTunnel", manager.setup_localtunnel),
        ("Serveo", manager.setup_serveo_tunnel)
    ]
    
    for service_name, setup_func in tunnel_services:
        print(f"\n🔧 {service_name} を試行中...")
        
        tunnel_url = setup_func()
        
        if tunnel_url:
            print(f"✅ {service_name} 設定成功!")
            print(f"🌐 Public URL: {tunnel_url}")
            
            # Webhook URL更新
            update_webhook_urls(tunnel_url)
            
            print(f"""
🎉 設定完了！

📋 次のステップ:
1. Error Monitor起動: python3 scripts/simple_error_monitor.py
2. テスト実行: curl -X POST {tunnel_url}/manual-test -d '{{"error":"test error"}}'
3. Netlify Webhook手動更新（上記URL参照）

🔄 PC再起動後の復旧:
このスクリプトを再実行すれば自動で復旧します
""")
            return tunnel_url
        
        print(f"❌ {service_name} 失敗、次のサービスを試行...")
    
    print("❌ 全てのトンネルサービス設定に失敗しました")
    return None

if __name__ == '__main__':
    main()