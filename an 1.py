using System;

namespace BankingSystem
{
    public class BankAccount
    {
        // 1. Static Field
        private static long _nextAccountNumber = 1000000001;

        // Constant
        private const decimal MIN_BALANCE = 50000m;

        // 2. Private Backing Fields
        private string _accountHolder = string.Empty;
        private decimal _balance;

        // 3. Properties
        public long AccountNumber { get; init; }

        public string AccountHolder
        {
            get => _accountHolder;
            set
            {
                if (string.IsNullOrWhiteSpace(value))
                {
                    throw new ArgumentException("Tên chủ tài khoản không được để trống hoặc null.");
                }
                _accountHolder = value;
            }
        }

        public decimal Balance
        {
            get => _balance;
            private set => _balance = value;
        }

        // 4. Constructor
        public BankAccount(string accountHolder, decimal initialBalance)
        {
            if (initialBalance < MIN_BALANCE)
            {
                throw new ArgumentException($"Số dư ban đầu tối thiểu phải từ {MIN_BALANCE:N0} VNĐ.");
            }

            AccountNumber = _nextAccountNumber++;
            AccountHolder = accountHolder;
            Balance = initialBalance;
        }

        // 5. Methods
        public void Deposit(decimal amount)
        {
            if (amount <= 0)
            {
                throw new ArgumentException("Số tiền nạp phải lớn hơn 0.");
            }
            Balance += amount;
            Console.WriteLine($"[Thành công] Nạp {amount:N0} VNĐ vào tài khoản {AccountNumber}.");
        }

        public bool Withdraw(decimal amount)
        {
            if (amount <= 0)
            {
                Console.WriteLine("[Lỗi] Số tiền rút phải lớn hơn 0.");
                return false;
            }

            if (Balance - amount < MIN_BALANCE)
            {
                Console.WriteLine($"[Thất bại] Rút {amount:N0} VNĐ không thành công. Số dư sau khi rút không được dưới {MIN_BALANCE:N0} VNĐ.");
                return false;
            }

            Balance -= amount;
            Console.WriteLine($"[Thành công] Rút {amount:N0} VNĐ từ tài khoản {AccountNumber}.");
            return true;
        }

        public void DisplayInfo()
        {
            Console.WriteLine("-----------------------------------");
            Console.WriteLine($"Số tài khoản : {AccountNumber}");
            Console.WriteLine($"Chủ tài khoản: {AccountHolder}");
            Console.WriteLine($"Số dư        : {Balance:N0} VNĐ");
            Console.WriteLine("-----------------------------------");
        }
    }

    internal class Program
    {
        private static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            Console.WriteLine("=== KIỂM THỨC TẠO TÀI KHOẢN ===");

            // Tạo 2 tài khoản hợp lệ
            BankAccount acc1 = new BankAccount("Nguyễn Văn A", 500000);
            BankAccount acc2 = new BankAccount("Trần Thị B", 1000000);

            acc1.DisplayInfo();
            acc2.DisplayInfo();

            // Thử khởi tạo tài khoản với số dư không hợp lệ (< 50,000 VNĐ)
            try
            {
                Console.WriteLine("\n[Thử nghiệm] Khởi tạo tài khoản với số dư 30,000 VNĐ...");
                BankAccount accInvalid = new BankAccount("Lê Văn C", 30000);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[Bắt lỗi exception]: {ex.Message}");
            }

            Console.WriteLine("\n=== KIỂM THỨC GIAO DỊCH (NẠP / RÚT) ===");

            // Nạp tiền hợp lệ
            acc1.Deposit(200000);
            
            // Rút tiền hợp lệ
            acc1.Withdraw(100000);

            // Rút tiền vi phạm hạn mức duy trì tối thiểu (50,000 VNĐ)
            acc1.Withdraw(600000);

            // Hiển thị thông tin cuối cùng
            Console.WriteLine("\n=== THÔNG TIN TÀI KHOẢN SAU GIAO DỊCH ===");
            acc1.DisplayInfo();
        }
    }
}