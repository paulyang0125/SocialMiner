class RedeemAPI {
    private $db;
 
    // Constructor - open DB connection
    function __construct() {
        $this->db = new mysqli('localhost', 'username', 'password', 'promos');
        $this->db->autocommit(FALSE);
    }
 
    // Destructor - close DB connection
    function __destruct() {
        $this->db->close();
    }
 
    // Main method to redeem a code
    function redeem() {
        // Print all codes in database
        $stmt = $this->db->prepare('SELECT id, code, unlock_code, uses_remaining FROM rw_promo_code');
        $stmt->execute();
        $stmt->bind_result($id, $code, $unlock_code, $uses_remaining);
        while ($stmt->fetch()) {
            echo "$code has $uses_remaining uses remaining!";
        }
        $stmt->close();
    }
}
