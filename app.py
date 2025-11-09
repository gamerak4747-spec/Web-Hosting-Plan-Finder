from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!

# Hosting plans data (Shared Hosting)
hosting_data = {
    "hostinger": {
        "Single": {
            "price": 69,
            "regular_price": 399,
            "websites": 1,
            "storage": "10 GB",
            "storage_value": 10,
            "type": "SSD",
            "bandwidth": "100 GB",
            "bandwidth_value": 100,
            "email": "1 Email",
            "free_domain": False,
            "ssl": "Free SSL",
            "cpanel": True,
            "backup": "Weekly Backups",
            "popular": False,
            "best_for": "Beginners"
        },
        "Premium": {
            "price": 149,
            "regular_price": 599,
            "websites": 100,
            "storage": "20 GB",
            "storage_value": 20,
            "type": "SSD",
            "bandwidth": "Unlimited",
            "bandwidth_value": float('inf'),
            "email": "Free Email",
            "free_domain": True,
            "ssl": "Free SSL",
            "cpanel": True,
            "backup": "Weekly Backups",
            "popular": True,
            "best_for": "Small businesses"
        },
        "Business": {
            "price": 249,
            "regular_price": 699,
            "websites": 100,
            "storage": "100 GB",
            "storage_value": 100,
            "type": "SSD",
            "bandwidth": "Unlimited",
            "bandwidth_value": float('inf'),
            "email": "Free Email",
            "free_domain": True,
            "ssl": "Free SSL",
            "cpanel": True,
            "backup": "Daily Backups",
            "popular": False,
            "best_for": "Growing businesses"
        }
    },
    "bluehost": {
        "Shared": {
            "price": 169,
            "regular_price": 299,
            "websites": 1,
            "storage": "50 GB",
            "storage_value": 50,
            "type": "SSD",
            "bandwidth": "Unmetered",
            "bandwidth_value": float('inf'),
            "email": "5 Email Accounts",
            "free_domain": True,
            "ssl": "Free SSL",
            "cpanel": True,
            "backup": "Basic Backup",
            "popular": True,
            "best_for": "Beginners"
        }
    },
    "godaddy": {
        "Economy": {
            "price": 219,
            "regular_price": 499,
            "websites": 1,
            "storage": "25 GB",
            "storage_value": 25,
            "type": "NVMe",
            "bandwidth": "Unmetered",
            "bandwidth_value": float('inf'),
            "email": "Free Email",
            "free_domain": True,
            "ssl": "Free SSL",
            "cpanel": True,
            "backup": "Basic Backup",
            "popular": False,
            "best_for": "Personal websites"
        }
    },
    "bigrock": {
        "Advanced": {
            "price": 159,
            "regular_price": 279,
            "websites": 1,
            "storage": "Unmetered",
            "storage_value": float('inf'),
            "type": "SSD",
            "bandwidth": "Unmetered",
            "bandwidth_value": float('inf'),
            "email": "Unlimited",
            "free_domain": True,
            "ssl": "Free SSL",
            "cpanel": True,
            "backup": "Daily Backups",
            "popular": True,
            "best_for": "Developed establishments"
        }
    },
    "namecheap": {
        "Stellar Plus": {
            "price": 204,
            "regular_price": 556,
            "websites": "Unlimited",
            "storage": "Unmetered",
            "storage_value": float('inf'),
            "type": "SSD",
            "bandwidth": "Unmetered",
            "bandwidth_value": float('inf'),
            "email": "Unlimited",
            "free_domain": True,
            "ssl": "Free SSL",
            "cpanel": True,
            "backup": "AutoBackup",
            "popular": True,
            "best_for": "Multiple websites"
        }
    }
}

# VPS hosting plans data
vps_data = {
    "hostinger": {
        "KVM 2": {
            "price": 749,
            "regular_price": 1599,
            "cpu_cores": 2,
            "ram": 8,
            "storage": "100 GB",
            "storage_value": 100,
            "type": "NVMe",
            "bandwidth": "8 TB",
            "bandwidth_value": 8000,
            "email": "Available",
            "free_domain": False,
            "ssl": "Free SSL",
            "backup": "Free weekly backups",
            "popular": True,
            "best_for": "Growing applications"
        }
    },
    "bluehost": {
        "Enhanced NVMe 8": {
            "price": 6299,
            "regular_price": 8695,
            "cpu_cores": 4,
            "ram": 8,
            "storage": "200 GB",
            "storage_value": 200,
            "type": "NVMe",
            "bandwidth": "Unmetered",
            "bandwidth_value": float('inf'),
            "email": "Available",
            "free_domain": False,
            "ssl": "Free SSL",
            "backup": "Daily Backups",
            "popular": True,
            "best_for": "More storage and customization"
        }
    },
    "bigrock": {
        "NVMe 8": {
            "price": 6838,
            "regular_price": 7500,
            "cpu_cores": 4,
            "ram": 8,
            "storage": "200 GB",
            "storage_value": 200,
            "type": "NVMe",
            "bandwidth": "3 TB",
            "bandwidth_value": 3000,
            "email": "Available",
            "free_domain": False,
            "ssl": "Free SSL",
            "backup": "Daily Backups",
            "popular": True,
            "best_for": "Business applications"
        }
    },
    "namecheap": {
        "Quasar": {
            "price": 1409,
            "regular_price": 1409,
            "cpu_cores": 4,
            "ram": 6,
            "storage": "120 GB",
            "storage_value": 120,
            "type": "SSD RAID 10",
            "bandwidth": "3 TB",
            "bandwidth_value": 3000,
            "email": "Available",
            "free_domain": False,
            "ssl": "Free SSL",
            "backup": "Daily Backups",
            "popular": True,
            "best_for": "Medium VPS projects"
        }
    }
}

# Buy Links for Shared Hosting
buy_links = {
    'hostinger': {
        'Single': 'https://www.hostinger.in/web-hosting',
        'Premium': 'https://www.hostinger.in/web-hosting',
        'Business': 'https://www.hostinger.in/web-hosting'
    },
    'bluehost': {
        'Shared': 'https://www.bluehost.in/hosting/shared'
    },
    'godaddy': {
        'Economy': 'https://www.godaddy.com/hosting/web-hosting'
    },
    'bigrock': {
        'Advanced': 'https://www.bigrock.in/web-hosting'
    },
    'namecheap': {
        'Stellar Plus': 'https://www.namecheap.com/hosting/shared/'
    }
}

# VPS Buy Links
vps_buy_links = {
    'hostinger': {
        'KVM 2': 'https://www.hostinger.in/vps-hosting'
    },
    'bluehost': {
        'Enhanced NVMe 8': 'https://www.bluehost.in/hosting/vps'
    },
    'bigrock': {
        'NVMe 8': 'https://www.bigrock.in/vps-hosting'
    },
    'namecheap': {
        'Quasar': 'https://www.namecheap.com/hosting/vps/'
    }
}

def calculate_score(plan, budget, websites, storage, need_email, need_domain, need_ssl):
    """Calculate a score for how well a plan matches requirements"""
    score = 0
    
    # Value for money
    value_ratio = 1 - (plan['price'] / budget) if budget > 0 else 0
    score += value_ratio * 30  # 30% weight for value
    
    # Storage match
    if plan['storage_value'] == float('inf'):
        storage_score = 1
    else:
        storage_ratio = min(plan['storage_value'] / storage, 2) / 2  # Cap at 2x requirement
        storage_score = storage_ratio
    score += storage_score * 20  # 20% weight for storage
    
    # Website allowance (only for shared hosting)
    if 'websites' in plan:
        if plan['websites'] == "Unlimited":
            website_score = 1
        else:
            website_ratio = min(plan['websites'] / websites, 2) / 2  # Cap at 2x requirement
            website_score = website_ratio
        score += website_score * 20  # 20% weight for websites
    else:
        score += 20  # Full score for VPS plans
    
    # Features
    feature_score = 0
    if need_domain and plan.get('free_domain', False):
        feature_score += 1
    if need_ssl and 'SSL' in plan.get('ssl', ''):
        feature_score += 1
    if need_email and plan.get('email', 'None') != "None":
        feature_score += 1
        
    # Normalize feature score
    needed_features = sum([need_domain, need_ssl, need_email])
    if needed_features > 0:
        feature_score = feature_score / needed_features
    else:
        feature_score = 1
        
    score += feature_score * 30  # 30% weight for features
    
    return score

@app.route('/', methods=['GET'])
def home():
    """Home page"""
    return render_template('home.html')

@app.route('/about')
def about():
    """About Us page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact Us page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just flash a success message
        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# FIXED: Changed function name from 'index' to 'calculator'
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    # Default form values
    form_data = {
        'websites': 1,
        'storage': 10,
        'budget': 200,
        'email': True,
        'domain': True,
        'ssl': True,
        'custom_plan': False,
        'hosting_type': 'shared'  # New field for hosting type
    }
    
    if request.method == 'POST':
        try:
            print("Form data received:", request.form)
            
            # Parse values from the form, handling potential parsing errors
            try:
                websites = int(request.form.get('websites', 1))
            except ValueError:
                websites = 1
                
            try:
                storage = int(request.form.get('storage', 10))
            except ValueError:
                storage = 10
                
            try:
                budget = int(request.form.get('budget', 200))
            except ValueError:
                budget = 200
            
            # Update form_data with submitted values
            form_data['websites'] = websites
            form_data['storage'] = storage
            form_data['budget'] = budget
            form_data['email'] = request.form.get('email') == 'on'
            form_data['domain'] = request.form.get('domain') == 'on'
            form_data['ssl'] = request.form.get('ssl') == 'on'
            form_data['custom_plan'] = request.form.get('custom_plan') == 'on'
            form_data['hosting_type'] = request.form.get('hosting_type', 'shared')
            
            print("Processed form_data:", form_data)
            
            # Select the appropriate data source based on hosting type
            if form_data['hosting_type'] == 'vps':
                data_source = vps_data
                links_source = vps_buy_links
            else:
                data_source = hosting_data
                links_source = buy_links
            
            # Find matching plans
            matching_plans = []
            
            for provider, plans in data_source.items():
                for plan_name, plan in plans.items():
                    # For VPS, check CPU/RAM requirements
                    if form_data['hosting_type'] == 'vps':
                        meets_requirements = (
                            plan['price'] <= budget and
                            (plan['storage_value'] == float('inf') or plan['storage_value'] >= storage)
                        )
                    else:
                        # For shared hosting, check website limits
                        meets_requirements = (
                            plan['price'] <= budget and
                            (plan['websites'] == "Unlimited" or plan['websites'] >= websites) and
                            (plan['storage_value'] == float('inf') or plan['storage_value'] >= storage) and
                            (not form_data['domain'] or plan['free_domain']) and
                            (not form_data['ssl'] or 'SSL' in plan['ssl'])
                        )
                    
                    if meets_requirements:
                        # Add buy link to the plan data
                        plan_with_link = plan.copy()
                        plan_with_link['buy_link'] = links_source.get(provider, {}).get(plan_name, '#')
                        
                        matching_plans.append({
                            'provider': provider,
                            'plan_name': plan_name,
                            'plan': plan_with_link,
                            'score': calculate_score(plan, budget, websites if form_data['hosting_type'] != 'vps' else 1, 
                                                   storage, form_data['email'], form_data['domain'], 
                                                   form_data['ssl'])
                        })
            
            # Sort plans by score (higher is better)
            matching_plans.sort(key=lambda x: x['score'], reverse=True)
            
            # Organize results
            result = {
                'best_plan': matching_plans[0] if matching_plans else None,
                'all_plans': matching_plans,
                'count': len(matching_plans),
                'hosting_type': form_data['hosting_type']
            }
            
            print(f"Found {len(matching_plans)} matching {form_data['hosting_type']} plans")
            
            return render_template('calculator.html', results=result, show_results=True, 
                                 form_data=form_data, buy_links=links_source)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return render_template('alculator.html', error=str(e), form_data=form_data)
    
    # For GET requests, show the form with default values
    return render_template('calculator.html', form_data=form_data)


@app.route('/compare', methods=['GET','POST'])
def compare():
    try:
        # Get user requirements from the form
        websites = int(request.form.get('websites', 1))
        storage = int(request.form.get('storage', 10))
        need_email = request.form.get('email') == 'on'
        need_domain = request.form.get('domain') == 'on'
        need_ssl = request.form.get('ssl') == 'on'
        budget = int(request.form.get('budget', 100))
        hosting_type = request.form.get('hosting_type', 'shared')
        
        print(f"Debug - Received form data: websites={websites}, storage={storage}, budget={budget}")
        print(f"Debug - Features: email={need_email}, domain={need_domain}, ssl={need_ssl}")
        print(f"Debug - Hosting type: {hosting_type}")
        
        # Select appropriate data source
        data_source = vps_data if hosting_type == 'vps' else hosting_data
        
        # Find matching plans
        matching_plans = []
        
        for provider, plans in data_source.items():
            for plan_name, plan in plans.items():
                # Different matching criteria for VPS and shared
                if hosting_type == 'vps':
                    meets_requirements = (
                        plan['price'] <= budget and
                        (plan['storage_value'] == float('inf') or plan['storage_value'] >= storage)
                    )
                else:
                    meets_requirements = (
                        plan['price'] <= budget and 
                        (plan['websites'] == "Unlimited" or plan['websites'] >= websites) and
                        (plan['storage_value'] == float('inf') or plan['storage_value'] >= storage) and
                        (not need_domain or plan['free_domain']) and
                        (not need_ssl or 'SSL' in plan['ssl'])
                    )
                
                if meets_requirements:
                    matching_plans.append({
                        'provider': provider,
                        'plan_name': plan_name,
                        'plan': plan,
                        'score': calculate_score(plan, budget, websites, storage, need_email, need_domain, need_ssl)
                    })
        
        print(f"Debug - Found {len(matching_plans)} matching plans")
        
        # Sort plans by score (higher is better)
        matching_plans.sort(key=lambda x: x['score'], reverse=True)
        
        # Organize results
        result = {
            'best_plan': matching_plans[0] if matching_plans else None,
            'all_plans': matching_plans,
            'count': len(matching_plans),
            'hosting_type': hosting_type
        }
        
        print(f"Debug - Sending response with {len(matching_plans)} plans")
        return jsonify(result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Debug - Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)