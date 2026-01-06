# Contributing to Hosts File Guardian

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly on Windows
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python test_guardian.py` (as administrator)

## Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

## Testing

- Always test as administrator
- Test both the direct process and service modes
- Verify file restoration works correctly
- Check log files for errors

## Reporting Issues

When reporting issues, please include:
- Windows version
- Python version
- Error messages from log files
- Steps to reproduce
- Expected vs actual behavior

