from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import TransactionRecord
import json, uuid, hashlib

MODULE_TITLE = 'Blockchain Security'

@login_required(login_url='login')
def index(request):
    total_transactions = TransactionRecord.objects.count()
    last_transaction = TransactionRecord.objects.order_by('-timestamp').first()
    return render(request, 'blockchain/index.html', {
        'title': MODULE_TITLE,
        'total_transactions': total_transactions,
        'last_transaction': last_transaction,
    })


@login_required(login_url='login')
def audit_dashboard(request):
    transactions = TransactionRecord.objects.order_by('-timestamp')[:12]
    total_transactions = TransactionRecord.objects.count()
    return render(request, 'blockchain/audit.html', {
        'title': 'Blockchain Audit',
        'transactions': transactions,
        'total_transactions': total_transactions,
    })


# Transaction CRUD

def list_transactions(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return JsonResponse(list(TransactionRecord.objects.order_by('-timestamp').values()), safe=False)


def create_transaction(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    tx_id = body.get('tx_id', str(uuid.uuid4()))
    sender = body.get('sender', 'nodeA')
    receiver = body.get('receiver', 'nodeB')
    amount = float(body.get('amount', 0.0))
    data = body.get('data', {})
    payload = json.dumps(data, sort_keys=True)
    tx_hash = hashlib.sha256(f"{tx_id}{sender}{receiver}{amount}{payload}".encode('utf-8')).hexdigest()
    data['tx_hash'] = tx_hash
    tx = TransactionRecord.objects.create(
        tx_id=tx_id,
        sender=sender,
        receiver=receiver,
        amount=amount,
        data=data,
    )
    return JsonResponse({'tx_id': tx.tx_id, 'tx_hash': tx_hash, 'status': 'recorded', 'immutable': True}, status=201)


def transaction_detail(request, tx_id):
    tx = get_object_or_404(TransactionRecord, tx_id=tx_id)
    if request.method == 'GET':
        return JsonResponse({'tx_id': tx.tx_id, 'sender': tx.sender, 'receiver': tx.receiver, 'amount': tx.amount, 'data': tx.data, 'timestamp': tx.timestamp})
    if request.method == 'DELETE':
        return JsonResponse({'error': 'immutable transactions cannot be deleted'}, status=405)
    return HttpResponseNotAllowed(['GET', 'DELETE'])


def audit_log(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    data = list(TransactionRecord.objects.order_by('-timestamp').values('tx_id', 'sender', 'receiver', 'amount', 'timestamp'))
    return JsonResponse({'audit': data}, safe=False)
